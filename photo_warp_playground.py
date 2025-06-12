import sys
import os
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QSlider, QHBoxLayout, QTextEdit
)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
import librosa
from PIL import Image
import cv2
import matplotlib.pyplot as plt
import io

from effects.photo_spectrogram import render as photo_warp_render

class PhotoWarpPlayground(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Photo Warp Playground")
        self.setMinimumSize(600, 500)
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

        # Slider voor tijdstip
        self.time_slider = QSlider(Qt.Orientation.Horizontal)
        self.time_slider.setMinimum(0)
        self.time_slider.setMaximum(100)
        self.time_slider.setValue(0)
        self.time_slider.valueChanged.connect(self.update_preview)
        self.time_label = QLabel("Tijd: 0.00s")
        time_layout = QHBoxLayout()
        time_layout.addWidget(self.time_label)
        time_layout.addWidget(self.time_slider)
        layout.addLayout(time_layout)

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

        # Preview
        self.preview = QLabel()
        self.preview.setFixedSize(400, 300)
        self.preview.setStyleSheet("border: 1px solid black;")
        layout.addWidget(self.preview)

        # Save knop
        self.save_btn = QPushButton("💾 Sla vervormde afbeelding op")
        self.save_btn.clicked.connect(self.save_image)
        self.save_btn.setEnabled(False)
        layout.addWidget(self.save_btn)

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
            self.time_slider.setMaximum(max(0, len(self.y) // self.sr - 1))
        except Exception as e:
            self.console.setPlainText(f"Audio laden mislukt: {e}")
            self.y = None
            self.sr = None

    def update_strength(self, value):
        self.strength = value / 100.0
        self.strength_label.setText(f"Effect sterkte: {self.strength:.2f}")
        self.update_preview()

    def update_preview(self):
        if not self.img_path or self.y is None or self.sr is None:
            self.preview.clear()
            self.save_btn.setEnabled(False)
            return
        t = self.time_slider.value()
        self.time_label.setText(f"Tijd: {t:.2f}s")
        start = t * self.sr
        chunk = self.y[int(start):int(start)+self.sr//15]  # ca. 1/15e seconde
        # Render met photo_warp_render
        fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
        ax.axis('off')
        try:
            photo_warp_render(ax, chunk, opacity=1.0, color="#FFFFFF", image_path=self.img_path, strength=self.strength)
            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
            plt.close(fig)
            buf.seek(0)
            img = Image.open(buf)
            qimg = QImage(img.tobytes(), img.width, img.height, QImage.Format.Format_RGBA8888)
            pixmap = QPixmap.fromImage(qimg).scaled(400, 300, Qt.AspectRatioMode.KeepAspectRatio)
            self.preview.setPixmap(pixmap)
            self.last_img = img
            self.save_btn.setEnabled(True)
        except Exception as e:
            self.console.setPlainText(f"Preview fout: {e}")
            self.preview.clear()
            self.save_btn.setEnabled(False)

    def save_image(self):
        if self.last_img is not None:
            file, _ = QFileDialog.getSaveFileName(self, "Sla afbeelding op", "vervormd.png", "PNG Files (*.png)")
            if file:
                self.last_img.save(file)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = PhotoWarpPlayground()
    gui.show()
    sys.exit(app.exec())
