import sys
import os
import glob
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QComboBox, QColorDialog, QLineEdit, QTextEdit, QSlider, QHBoxLayout
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap, QMovie
import subprocess
import re

class PhotoSpectroPreviewThread(QThread):
    log_signal = pyqtSignal(str)
    done_signal = pyqtSignal(bool, str)
    progress_signal = pyqtSignal(int)
    max_progress_signal = pyqtSignal(int)

    def __init__(self, cmd, output_name):
        super().__init__()
        self.cmd = cmd
        self.output_name = output_name

    def run(self):
        try:
            with subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1) as proc:
                for line in proc.stdout:
                    self.log_signal.emit(line.rstrip())
                    m = re.search(r"Frame (\d+)/(\d+)", line)
                    if m:
                        self.progress_signal.emit(int(m.group(1)))
                        self.max_progress_signal.emit(int(m.group(2)))
                proc.wait()
                if proc.returncode == 0:
                    self.done_signal.emit(True, os.path.abspath(self.output_name))
                else:
                    self.done_signal.emit(False, "❌ Geen output bestand")
        except Exception as e:
            self.done_signal.emit(False, f"❌ Error: {e}")

class PhotoSpectroGUI(QWidget):
    thread_created = pyqtSignal(QThread)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Photo Spectrogram Preview")
        self.setMinimumSize(400, 360)
        layout = QVBoxLayout()

        # Audio file
        self.audio_btn = QPushButton("🎵 Kies audio (.mp3/.wav)")
        self.audio_btn.clicked.connect(self.choose_audio)
        self.audio_path = ""
        layout.addWidget(self.audio_btn)

        # Foto
        self.img_btn = QPushButton("🖼️ Kies foto")
        self.img_btn.clicked.connect(self.choose_img)
        self.img_path = ""
        layout.addWidget(self.img_btn)

        # Kleur
        self.color = "#FFFFFF"
        self.color_btn = QPushButton("🌈 Kies spectrogram kleur")
        self.color_btn.clicked.connect(self.pick_color)
        layout.addWidget(self.color_btn)

        # Output naam
        self.output_input = QLineEdit()
        self.output_input.setPlaceholderText("previews/photo_spectrogram_preview.mp4 (optioneel)")
        layout.addWidget(self.output_input)

        # Effect strength slider
        self.strength = 0.5
        slider_layout = QHBoxLayout()
        self.strength_label = QLabel("Effect sterkte: 0.5")
        self.strength_slider = QSlider(Qt.Orientation.Horizontal)
        self.strength_slider.setMinimum(0)
        self.strength_slider.setMaximum(100)
        self.strength_slider.setValue(50)
        self.strength_slider.valueChanged.connect(self.update_strength)
        slider_layout.addWidget(self.strength_label)
        slider_layout.addWidget(self.strength_slider)
        layout.addLayout(slider_layout)

        # Preview GIF
        self.preview = QLabel()
        self.preview.setFixedSize(240, 135)
        self.preview.setStyleSheet("border: 1px solid black;")
        gif_path = "previews1/spectrogram_photo.gif"
        if os.path.exists(gif_path):
            movie = QMovie(gif_path)
            movie.setScaledSize(self.preview.size())
            self.preview.setMovie(movie)
            movie.start()
        layout.addWidget(self.preview)

        # Start knop
        self.run_btn = QPushButton("▶️ Genereer Preview")
        self.run_btn.clicked.connect(self.run_preview)
        layout.addWidget(self.run_btn)

        # Console
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setMinimumHeight(40)
        layout.addWidget(self.console)

        # Log
        self.log = QLineEdit()
        self.log.setReadOnly(True)
        layout.addWidget(self.log)

        self.setLayout(layout)

    def choose_audio(self):
        file, _ = QFileDialog.getOpenFileName(self, "Kies audio", "", "Audio Files (*.mp3 *.wav)")
        if file:
            self.audio_path = file
            self.audio_btn.setText(f"🎵 {os.path.basename(file)}")

    def choose_img(self):
        file, _ = QFileDialog.getOpenFileName(self, "Kies foto", "", "Afbeeldingen (*.jpg *.jpeg *.png *.bmp)")
        if file:
            self.img_path = file
            self.img_btn.setText(f"🖼️ {os.path.basename(file)}")

    def pick_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = color.name()
            self.color_btn.setStyleSheet(f"background-color: {self.color};")

    def update_strength(self, value):
        self.strength = value / 100.0
        self.strength_label.setText(f"Effect sterkte: {self.strength:.2f}")

    def run_preview(self):
        if not self.audio_path or not self.img_path:
            self.console.setPlainText("⚠️ Kies zowel audio als foto!")
            return
        output_name = self.output_input.text().strip() or "previews/photo_spectrogram_preview.mp4"
        cmd = [
            sys.executable, "preview_mp4.py", self.audio_path, "photo_spectrogram",
            "--color", self.color,
            "--image", self.img_path,
            "--output", output_name,
            "--strength", str(self.strength)
        ]
        self.console.setPlainText(f"▶️ Running: {' '.join(cmd)}")
        self.log.setText("")
        self.run_btn.setEnabled(False)
        self.thread = PhotoSpectroPreviewThread(cmd, output_name)
        self.thread.log_signal.connect(lambda msg: self.console.append(msg))
        self.thread.progress_signal.connect(self.update_progress)
        self.thread.max_progress_signal.connect(self.set_progress_max)
        self.thread_created.emit(self.thread)
        def on_done(success, logmsg):
            self.log.setText(logmsg)
            self.run_btn.setEnabled(True)
        self.thread.done_signal.connect(on_done)
        self.thread.start()

    def update_progress(self, value):
        pass

    def set_progress_max(self, value):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = PhotoSpectroGUI()
    gui.show()
    sys.exit(app.exec())
