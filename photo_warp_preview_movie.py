import sys
import os
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QSlider, QHBoxLayout, QTextEdit, QLineEdit
)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
import librosa
from PIL import Image
import cv2
import matplotlib.pyplot as plt
import io
import tempfile
import subprocess
from effects.photo_spectrogram import render as photo_warp_render

class PhotoWarpPreviewMovie(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Photo Warp Preview Movie")
        self.setMinimumSize(600, 520)
        layout = QVBoxLayout()

        # Foto kiezen
        self.img_btn = QPushButton("🖼️ Kies foto")
        self.img_btn.clicked.connect(self.choose_img)
        self.img_path = ""
        layout.addWidget(self.img_btn)

        # Audio kiezen
        self.audio_btn = QPushButton("🎵 Kies audio (.mp3/.wav)")
        self.audio_btn.clicked.connect(self.choose_audio)
        self.audio_path = ""
        layout.addWidget(self.audio_btn)

        # Slider voor strength
        self.strength = 0.5
        self.strength_slider = QSlider(Qt.Orientation.Horizontal)
        self.strength_slider.setMinimum(0)
        self.strength_slider.setMaximum(100)
        self.strength_slider.setValue(50)
        self.strength_slider.valueChanged.connect(self.update_strength)
        self.strength_label = QLabel("Effect sterkte: 0.5")
        strength_layout = QHBoxLayout()
        strength_layout.addWidget(self.strength_label)
        strength_layout.addWidget(self.strength_slider)
        layout.addLayout(strength_layout)

        # Slider voor opacity
        self.opacity = 0.85
        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setMinimum(0)
        self.opacity_slider.setMaximum(100)
        self.opacity_slider.setValue(int(self.opacity * 100))
        self.opacity_slider.valueChanged.connect(self.update_opacity)
        self.opacity_label = QLabel("Opacity: 0.85")
        opacity_layout = QHBoxLayout()
        opacity_layout.addWidget(self.opacity_label)
        opacity_layout.addWidget(self.opacity_slider)
        layout.addLayout(opacity_layout)

        # Preview
        self.preview = QLabel()
        self.preview.setFixedSize(400, 300)
        self.preview.setStyleSheet("border: 1px solid black;")
        layout.addWidget(self.preview)

        # Output naam
        self.output_input = QLineEdit()
        self.output_input.setPlaceholderText("previews/photo_warp_preview.mp4 (optioneel)")
        layout.addWidget(self.output_input)

        # Genereer video knop
        self.run_btn = QPushButton("▶️ Genereer Preview Video")
        self.run_btn.clicked.connect(self.run_preview_movie)
        layout.addWidget(self.run_btn)

        # Console
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setMinimumHeight(40)
        layout.addWidget(self.console)

        self.setLayout(layout)
        self.y = None
        self.sr = None
        self.last_img = None

    def choose_img(self):
        file, _ = QFileDialog.getOpenFileName(self, "Kies foto", "", "Afbeeldingen (*.jpg *.jpeg *.png *.bmp)")
        if file:
            self.img_path = file
            self.img_btn.setText(f"🖼️ {os.path.basename(file)}")
            self.update_preview()

    def choose_audio(self):
        file, _ = QFileDialog.getOpenFileName(self, "Kies audio", "", "Audio Files (*.mp3 *.wav)")
        if file:
            self.audio_path = file
            self.audio_btn.setText(f"🎵 {os.path.basename(file)}")
            self.load_audio()
            self.update_preview()

    def load_audio(self):
        try:
            self.y, self.sr = librosa.load(self.audio_path, sr=44100)
        except Exception as e:
            self.console.setPlainText(f"Audio laden mislukt: {e}")
            self.y = None
            self.sr = None

    def update_strength(self, value):
        self.strength = value / 100.0
        self.strength_label.setText(f"Effect sterkte: {self.strength:.2f}")
        self.update_preview()

    def update_opacity(self, value):
        self.opacity = value / 100.0
        self.opacity_label.setText(f"Opacity: {self.opacity:.2f}")
        self.update_preview()

    def update_preview(self):
        if not self.img_path or self.y is None or self.sr is None:
            self.preview.clear()
            return
        t = 0
        start = t * self.sr
        chunk = self.y[int(start):int(start)+self.sr//15]  # ca. 1/15e seconde
        fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
        ax.axis('off')
        try:
            photo_warp_render(ax, chunk, opacity=self.opacity, color="#FFFFFF", image_path=self.img_path, strength=self.strength)
            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
            plt.close(fig)
            buf.seek(0)
            img = Image.open(buf)
            qimg = QImage(img.tobytes(), img.width, img.height, QImage.Format.Format_RGBA8888)
            pixmap = QPixmap.fromImage(qimg).scaled(400, 300, Qt.AspectRatioMode.KeepAspectRatio)
            self.preview.setPixmap(pixmap)
            self.last_img = img
        except Exception as e:
            self.console.setPlainText(f"Preview fout: {e}")
            self.preview.clear()

    def run_preview_movie(self):
        if not self.img_path or self.y is None or self.sr is None:
            self.console.setPlainText("⚠️ Kies zowel audio als foto!")
            return
        output_name = self.output_input.text().strip() or "previews/photo_warp_preview.mp4"
        duration = min(5, int(len(self.y) / self.sr))  # max 5 seconden
        fps = 15
        self.console.setPlainText("Frames renderen...")
        with tempfile.TemporaryDirectory() as tmpdir:
            frame_paths = []
            for i in range(duration * fps):
                start = int(i * self.sr / fps)
                chunk = self.y[start:start+self.sr//fps]
                fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
                ax.axis('off')
                try:
                    photo_warp_render(ax, chunk, opacity=self.opacity, color="#FFFFFF", image_path=self.img_path, strength=self.strength)
                    frame_path = os.path.join(tmpdir, f"frame_{i:05d}.png")
                    plt.savefig(frame_path, format='png', bbox_inches='tight', pad_inches=0)
                    plt.close(fig)
                    frame_paths.append(frame_path)
                except Exception as e:
                    self.console.append(f"Frame {i}: {e}")
            # Maak video van frames
            video_path = os.path.join(tmpdir, "preview.mp4")
            cmd = [
                "ffmpeg", "-y", "-framerate", str(fps),
                "-i", os.path.join(tmpdir, "frame_%05d.png"),
                "-c:v", "libx264", "-pix_fmt", "yuv420p", video_path
            ]
            self.console.append("Video genereren met ffmpeg...")
            subprocess.run(cmd)
            # Voeg audio toe
            cmd = [
                "ffmpeg", "-y",
                "-i", video_path,
                "-ss", "0", "-t", str(duration),
                "-i", self.audio_path,
                "-map", "0:v:0", "-map", "1:a:0",
                "-c:v", "copy", "-c:a", "aac", "-shortest",
                output_name
            ]
            self.console.append("Audio toevoegen...")
            subprocess.run(cmd)
            self.console.append(f"✅ Preview opgeslagen als: {output_name}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = PhotoWarpPreviewMovie()
    gui.show()
    sys.exit(app.exec())
