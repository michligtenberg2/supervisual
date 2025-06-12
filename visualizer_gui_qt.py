import os
import sys
import glob
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog,
    QLabel, QComboBox, QColorDialog, QHBoxLayout, QLineEdit, QTextEdit, QProgressBar
)
from PyQt6.QtGui import QPixmap, QColor
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import subprocess


def get_available_effects(effects_dir="effects"):
    if not os.path.exists(effects_dir):
        return []
    return [
        f.replace(".py", "")
        for f in os.listdir(effects_dir)
        if f.endswith(".py") and not f.startswith("__")
    ]


class RenderThread(QThread):
    progress_signal = pyqtSignal(int)
    max_progress_signal = pyqtSignal(int)
    log_signal = pyqtSignal(str)
    done_signal = pyqtSignal(bool, str)

    def __init__(self, cmd, output_name):
        super().__init__()
        self.cmd = cmd
        self.output_name = output_name

    def run(self):
        import re
        try:
            with subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1) as proc:
                for line in proc.stdout:
                    self.log_signal.emit(line.rstrip())
                    if "Rendering" in line and "frames" in line:
                        m = re.search(r"Rendering (\\d+) frames", line)
                        if m:
                            self.max_progress_signal.emit(int(m.group(1)))
                    m = re.search(r"Frame (\\d+)/(\\d+)", line)
                    if m:
                        self.progress_signal.emit(int(m.group(1)))
                proc.wait()
                if proc.returncode == 0:
                    self.done_signal.emit(True, os.path.abspath(self.output_name))
                else:
                    self.done_signal.emit(False, "❌ Geen output bestand")
        except Exception as e:
            self.done_signal.emit(False, f"❌ Error: {e}")


class VisualizerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧱 Supervisual (by mich)")
        self.setStyleSheet("background-color: #dddddd; font-family: monospace;")
        self.setMinimumSize(500, 500)
        layout = QVBoxLayout()

        # Effect selector
        self.effect_label = QLabel("🎨 Effect:")
        self.effect_dropdown = QComboBox()
        available_effects = sorted([
            os.path.splitext(os.path.basename(f))[0]
            for f in glob.glob("effects/*.py")
            if not f.endswith("__init__.py")
        ])
        available_previews = {
            os.path.splitext(os.path.basename(f))[0]
            for f in glob.glob("previews/*.gif")
        }
        effects_with_previews = [e for e in available_effects if e in available_previews]
        self.effect_dropdown.addItems(available_effects)
        self.effect_dropdown.currentTextChanged.connect(self.update_preview)

        # Preview
        self.preview = QLabel()
        self.preview.setFixedSize(240, 135)
        self.preview.setStyleSheet("border: 1px solid black;")
        self.update_preview(self.effect_dropdown.currentText())

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
        layout.addWidget(self.transparent_checkbox)

        # File chooser
        self.file_button = QPushButton("📂 Kies video")
        self.file_button.clicked.connect(self.choose_file)
        self.input_path = ""

        # Output name
        self.output_input = QLineEdit()
        self.output_input.setPlaceholderText("output_supervisual.mp4")

        # Start button
        self.run_button = QPushButton("▶️ Start visualisatie")
        self.run_button.clicked.connect(self.run_visual_engine)
        # Cancel button
        self.cancel_button = QPushButton("❌ Stoppen")
        self.cancel_button.setEnabled(False)
        self.cancel_button.clicked.connect(self.cancel_render)

        # Console output (log)
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setStyleSheet("background-color: #222; color: #0f0; font-family: monospace; padding: 8px;")
        self.console.setMinimumHeight(80)
        # Log output
        self.log = QLineEdit()
        self.log.setReadOnly(True)
        self.log.setStyleSheet("background-color: #111; color: #fff; font-family: monospace; padding: 4px;")

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        self.progress.setValue(0)
        layout.addWidget(self.progress)

        # Layout (move console and log to bottom)
        layout.addWidget(self.effect_label)
        layout.addWidget(self.effect_dropdown)
        layout.addWidget(self.preview)
        layout.addWidget(self.color_button)
        layout.addWidget(self.bg_btn)
        layout.addWidget(self.file_button)
        layout.addWidget(QLabel("💾 Bestandsnaam (inclusief .mp4):"))
        layout.addWidget(self.output_input)
        layout.addWidget(self.run_button)
        layout.addWidget(self.cancel_button)
        # Move these to the bottom
        layout.addWidget(QLabel("🖥️ Console output:"))
        layout.addWidget(self.console)
        layout.addWidget(QLabel("📜 Log bestand (laatste pad):"))
        layout.addWidget(self.log)
        self.setLayout(layout)

    def update_preview(self, effect_name):
        gif_path = f"previews1/{effect_name}.gif"
        if os.path.exists(gif_path):
            self.preview.setPixmap(QPixmap(gif_path).scaled(240, 135, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            self.preview.clear()

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

    def choose_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Kies video", "", "Video Files (*.mp4 *.mov *.avi)")
        if file:
            self.input_path = file
            self.file_button.setText(f"📂 {os.path.basename(file)}")

    def run_visual_engine(self):
        if not self.input_path:
            self.console.setPlainText("⚠️ Geen inputbestand gekozen")
            return
        effect = self.effect_dropdown.currentText()
        fps = 30
        opacity = 0.65
        color = self.color
        bg_color = self.bg_color if not self.transparent_bg else "transparent"
        output_name = self.output_input.text().strip() or "output_supervisual.mp4"
        cmd = [
            sys.executable, "main.py", self.input_path,
            "--effects", effect,
            "--fps", str(fps),
            "--opacity", str(opacity),
            "--color", color,
            "--output", output_name,
            "--background", bg_color
        ]
        self.console.setPlainText(f"▶️ Running: {' '.join(cmd)}")
        self.progress.setValue(0)
        self.progress.setMaximum(100)
        self.log.setText("")
        self.run_button.setEnabled(False)
        self.cancel_button.setEnabled(True)
        self.render_thread = RenderThread(cmd, output_name)
        self.render_thread.progress_signal.connect(self.progress.setValue)
        self.render_thread.max_progress_signal.connect(self.progress.setMaximum)
        self.render_thread.log_signal.connect(lambda msg: self.console.append(msg))
        def on_done(success, logmsg):
            self.log.setText(logmsg)
            self.run_button.setEnabled(True)
            self.cancel_button.setEnabled(False)
            if success:
                self.progress.setValue(self.progress.maximum())
            else:
                self.progress.setValue(0)
        self.render_thread.done_signal.connect(on_done)
        self.render_thread.start()

    def cancel_render(self):
        if hasattr(self, 'render_thread') and self.render_thread.isRunning():
            self.render_thread.terminate()
            self.console.append("❌ Rendering gestopt door gebruiker.")
            self.run_button.setEnabled(True)
            self.cancel_button.setEnabled(False)
            self.progress.setValue(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = VisualizerGUI()
    gui.show()
    sys.exit(app.exec())
