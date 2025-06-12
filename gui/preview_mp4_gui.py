import os
import sys
import glob
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog,
    QLabel, QComboBox, QColorDialog, QLineEdit, QTextEdit, QHBoxLayout
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import subprocess
import re

class PreviewThread(QThread):
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

class PreviewMP4GUI(QWidget):
    thread_created = pyqtSignal(QThread)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎬 MP4 Preview Generator")
        self.setStyleSheet("background-color: #eeeeee; font-family: monospace;")
        self.setMinimumSize(400, 350)
        layout = QVBoxLayout()

        # Effect selector
        self.effect_label = QLabel("🎨 Effect:")
        self.effect_dropdown = QComboBox()
        available_effects = sorted([
            os.path.splitext(os.path.basename(f))[0]
            for f in glob.glob("effects/*.py")
            if not f.endswith("__init__.py")
        ])
        self.effect_dropdown.addItems(available_effects)

        # Audio file chooser
        self.audio_button = QPushButton("🎵 Kies audio (.mp3/.wav)")
        self.audio_button.clicked.connect(self.choose_audio)
        self.audio_path = ""

        # Color picker
        self.color = "#FFFFFF"
        self.color_button = QPushButton("🌈 Kies kleur")
        self.color_button.clicked.connect(self.pick_color)

        # Background color picker
        self.bg_color = "#000000"
        self.bg_btn = QPushButton("🌄 Kies achtergrondkleur")
        self.bg_btn.clicked.connect(self.choose_bg_color)
        self.bg_btn.setStyleSheet(f"background-color: {self.bg_color};")

        # Background transparency toggle
        self.transparent_bg = False
        self.transparent_checkbox = QPushButton("Transparante achtergrond uit")
        self.transparent_checkbox.setCheckable(True)
        self.transparent_checkbox.setChecked(False)
        self.transparent_checkbox.clicked.connect(self.toggle_transparent_bg)

        # Output name
        self.output_input = QLineEdit()
        self.output_input.setPlaceholderText("previews/<effect>_preview.mp4 (optioneel)")

        # Generate button
        self.run_button = QPushButton("▶️ Genereer MP4 Preview")
        self.run_button.clicked.connect(self.run_preview)

        # Console output
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setStyleSheet("background-color: #222; color: #0f0; font-family: monospace; padding: 8px;")
        self.console.setMinimumHeight(60)

        # Log output
        self.log = QLineEdit()
        self.log.setReadOnly(True)
        self.log.setStyleSheet("background-color: #111; color: #fff; font-family: monospace; padding: 4px;")

        # Layout
        layout.addWidget(self.effect_label)
        layout.addWidget(self.effect_dropdown)
        layout.addWidget(self.audio_button)
        layout.addWidget(self.color_button)
        layout.addWidget(self.bg_btn)
        layout.addWidget(self.transparent_checkbox)
        layout.addWidget(QLabel("💾 Bestandsnaam (optioneel):"))
        layout.addWidget(self.output_input)
        layout.addWidget(self.run_button)
        layout.addWidget(QLabel("🖥️ Console output:"))
        layout.addWidget(self.console)
        layout.addWidget(QLabel("📜 Log bestand (laatste pad):"))
        layout.addWidget(self.log)
        self.setLayout(layout)

    def choose_audio(self):
        file, _ = QFileDialog.getOpenFileName(self, "Kies audio", "", "Audio Files (*.mp3 *.wav)")
        if file:
            self.audio_path = file
            self.audio_button.setText(f"🎵 {os.path.basename(file)}")

    def pick_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = color.name()
            self.color_button.setStyleSheet(f"background-color: {self.color};")

    def choose_bg_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.bg_color = color.name()
            self.bg_btn.setStyleSheet(f"background-color: {self.bg_color};")

    def toggle_transparent_bg(self):
        self.transparent_bg = not self.transparent_bg
        if self.transparent_bg:
            self.transparent_checkbox.setText("Transparante achtergrond aan")
            self.bg_color = "transparent"
            self.bg_btn.setEnabled(False)
        else:
            self.transparent_checkbox.setText("Transparante achtergrond uit")
            self.bg_color = "#000000"
            self.bg_btn.setEnabled(True)
            self.bg_btn.setStyleSheet(f"background-color: {self.bg_color};")

    def run_preview(self):
        if not self.audio_path:
            self.console.setPlainText("⚠️ Geen audio gekozen")
            return
        effect = self.effect_dropdown.currentText()
        color = self.color
        bg_color = self.bg_color if not self.transparent_bg else "transparent"
        output_name = self.output_input.text().strip()
        cmd = [
            sys.executable, "preview_mp4.py", self.audio_path, effect,
            "--color", color,
            "--background", bg_color
        ]
        if self.transparent_bg:
            cmd.append("--transparent")
        if output_name:
            cmd.extend(["--output", output_name])
        self.console.setPlainText(f"▶️ Running: {' '.join(cmd)}")
        self.log.setText("")
        self.run_button.setEnabled(False)
        self.preview_thread = PreviewThread(cmd, output_name or f"previews/{effect}_preview.mp4")
        self.preview_thread.log_signal.connect(lambda msg: self.console.append(msg))
        self.preview_thread.progress_signal.connect(self.update_progress)
        self.preview_thread.max_progress_signal.connect(self.set_progress_max)
        self.thread_created.emit(self.preview_thread)
        def on_done(success, logmsg):
            self.log.setText(logmsg)
            self.run_button.setEnabled(True)
        self.preview_thread.done_signal.connect(on_done)
        self.preview_thread.start()

    def update_progress(self, value):
        pass

    def set_progress_max(self, value):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = PreviewMP4GUI()
    gui.show()
    sys.exit(app.exec())
