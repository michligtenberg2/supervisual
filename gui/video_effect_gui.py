import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QComboBox, QColorDialog, QLineEdit, QTextEdit, QSlider, QHBoxLayout
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import subprocess
import glob
import re

class VideoEffectThread(QThread):
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

class VideoEffectGUI(QWidget):
    thread_created = pyqtSignal(QThread)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Effect + Audio-reactive Overlay")
        self.setMinimumSize(420, 400)
        layout = QVBoxLayout()

        # Video file
        self.video_btn = QPushButton("🎬 Kies video (.mp4)")
        self.video_btn.clicked.connect(self.choose_video)
        self.video_path = ""
        layout.addWidget(self.video_btn)

        # Audio file
        self.audio_btn = QPushButton("🎵 Kies audio (.mp3/.wav, optioneel)")
        self.audio_btn.clicked.connect(self.choose_audio)
        self.audio_path = ""
        layout.addWidget(self.audio_btn)

        # Effect selector
        self.effect_label = QLabel("🎨 Effect:")
        self.effect_dropdown = QComboBox()
        available_effects = sorted([
            os.path.splitext(os.path.basename(f))[0]
            for f in glob.glob("effects/*.py")
            if not f.endswith("__init__.py")
        ])
        self.effect_dropdown.addItems(available_effects)
        layout.addWidget(self.effect_label)
        layout.addWidget(self.effect_dropdown)

        # Kleur
        self.color = "#FFFFFF"
        self.color_btn = QPushButton("🌈 Kies effectkleur")
        self.color_btn.clicked.connect(self.pick_color)
        layout.addWidget(self.color_btn)

        # Output naam
        output_layout = QHBoxLayout()
        self.output_input = QLineEdit()
        self.output_input.setPlaceholderText("output/video_effect_overlay.mp4 (optioneel)")
        output_layout.addWidget(self.output_input)
        self.output_btn = QPushButton("💾 Kies output-bestand")
        self.output_btn.clicked.connect(self.choose_output_file)
        output_layout.addWidget(self.output_btn)
        layout.addLayout(output_layout)

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

        # Start knop
        self.run_btn = QPushButton("▶️ Genereer Video met Effect")
        self.run_btn.clicked.connect(self.run_effect)
        layout.addWidget(self.run_btn)

        # Console
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setMinimumHeight(60)
        layout.addWidget(self.console)

        # Log
        self.log = QLineEdit()
        self.log.setReadOnly(True)
        layout.addWidget(self.log)

        self.setLayout(layout)

    def choose_video(self):
        file, _ = QFileDialog.getOpenFileName(self, "Kies video", "", "Video Files (*.mp4 *.mov *.avi)")
        if file:
            self.video_path = file
            self.video_btn.setText(f"🎬 {os.path.basename(file)}")

    def choose_audio(self):
        file, _ = QFileDialog.getOpenFileName(self, "Kies audio", "", "Audio Files (*.mp3 *.wav)")
        if file:
            self.audio_path = file
            self.audio_btn.setText(f"🎵 {os.path.basename(file)}")

    def pick_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = color.name()
            self.color_btn.setStyleSheet(f"background-color: {self.color};")

    def update_strength(self, value):
        self.strength = value / 100.0
        self.strength_label.setText(f"Effect sterkte: {self.strength:.2f}")

    def choose_output_file(self):
        file, _ = QFileDialog.getSaveFileName(self, "Kies output-bestand", "output/video_effect_overlay.mp4", "Video Files (*.mp4)")
        if file:
            self.output_input.setText(file)

    def run_effect(self):
        if not self.video_path:
            self.console.setPlainText("⚠️ Kies een video!")
            return
        effect = self.effect_dropdown.currentText()
        color = self.color
        output_name = self.output_input.text().strip() or "output/video_effect_overlay.mp4"
        # If output_name is just a filename (no directory), save to output/ by default
        if not os.path.dirname(output_name):
            output_name = os.path.join("output", output_name)
        os.makedirs(os.path.dirname(output_name), exist_ok=True)
        cmd = [
            sys.executable, "main.py", self.video_path,
            "--effects", effect,
            "--color", color,
            "--output", output_name,
            "--strength", str(self.strength)
        ]
        if self.audio_path:
            cmd.extend(["--audio", self.audio_path])
        self.console.setPlainText(f"▶️ Running: {' '.join(cmd)}")
        self.log.setText("")
        self.run_btn.setEnabled(False)
        self.thread = VideoEffectThread(cmd, output_name)
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
        # For local progress bar, if any. For mega-tool, signal is already connected.
        pass

    def set_progress_max(self, value):
        # For local progress bar, if any. For mega-tool, signal is already connected.
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = VideoEffectGUI()
    gui.show()
    sys.exit(app.exec())
