import os
import sys
import glob
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog,
    QLabel, QComboBox, QSlider, QColorDialog, QHBoxLayout, QTextEdit, QLineEdit
)

from PyQt6.QtGui import QPixmap, QColor
from PyQt6.QtCore import Qt
def get_available_effects(effects_dir="effects"):
    if not os.path.exists(effects_dir):
        return []
    return [
        f.replace(".py", "")
        for f in os.listdir(effects_dir)
        if f.endswith(".py") and not f.startswith("__")
    ]

class VisualizerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧱 Supervisual (by mich)")
        self.setStyleSheet("background-color: #dddddd; font-family: monospace;")
        self.setMinimumSize(500, 500)
        layout = QVBoxLayout()
        # Effect selector (koppelt aan zowel effects/*.py en previews/*.gif)
        self.effect_label = QLabel("🎨 Effect:")
        self.effect_dropdown = QComboBox()

        self.output_input = QLineEdit()
        self.output_input.setPlaceholderText("output_supervisual.mp4")
        
        self.setLayout(layout)        
        
        # Zoek alle effect modules
        available_effects = sorted([
        os.path.splitext(os.path.basename(f))[0]
    for f in glob.glob("effects/*.py")
    if not f.endswith("__init__.py")
])

        # Zoek alle beschikbare preview gifs
        available_previews = {
    os.path.splitext(os.path.basename(f))[0]
    for f in glob.glob("previews/*.gif")
}

        # Voeg alleen effecten toe die óók een preview hebben
        effects_with_previews = [e for e in available_effects if e in available_previews]
        self.effect_dropdown.addItems(available_effects)
        self.effect_dropdown.currentTextChanged.connect(self.update_preview)  # Correcte regel zonder extra haakje
        # Preview
        self.preview = QLabel()
        self.preview.setFixedSize(240, 135)
        self.preview.setStyleSheet("border: 1px solid black;")
        self.update_preview(self.effect_dropdown.currentText())

        # FPS slider
        self.fps_slider = QSlider(Qt.Orientation.Horizontal)
        self.fps_slider.setMinimum(10)
        self.fps_slider.setMaximum(60)
        self.fps_slider.setValue(30)
        self.fps_label = QLabel("🎞️ FPS: 30")
        self.fps_slider.valueChanged.connect(lambda v: self.fps_label.setText(f"🎞️ FPS: {v}"))

        # Opacity slider
        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setMinimum(10)
        self.opacity_slider.setMaximum(100)
        self.opacity_slider.setValue(65)
        self.opacity_label = QLabel("🫧 Opacity: 65%")
        self.opacity_slider.valueChanged.connect(lambda v: self.opacity_label.setText(f"🫧 Opacity: {v}%"))

        # Color picker
        self.color = "#FFFFFF"
        self.color_button = QPushButton("🌈 Kies kleur")
        self.color_button.clicked.connect(self.pick_color)

        self.bg_btn = QPushButton("🌄 Kies achtergrondkleur")
        self.bg_btn.clicked.connect(self.choose_bg_color)
        self.bg_color = "#000000"  # <- voeg deze regel toe

        # Bestand kiezen
        self.file_button = QPushButton("📂 Kies video")
        self.file_button.clicked.connect(self.choose_file)
        self.input_path = ""

        self.output_input = QLineEdit()
        self.output_input.setPlaceholderText("output_supervisual.mp4")
        layout.addWidget(QLabel("💾 Bestandsnaam (inclusief .mp4):"))
        layout.addWidget(self.output_input)

        # Start knop
        self.run_button = QPushButton("▶️ Start visualisatie")
        self.run_button.clicked.connect(self.run_visual_engine)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.effect_label)
        layout.addWidget(self.effect_dropdown)
        layout.addWidget(self.preview)
        layout.addWidget(self.fps_label)
        layout.addWidget(self.fps_slider)
        layout.addWidget(self.opacity_label)
        layout.addWidget(self.opacity_slider)
        layout.addWidget(self.color_button)
        layout.addWidget(self.bg_btn)
        layout.addWidget(self.file_button)
        layout.addWidget(QLabel("💾 Bestandsnaam (inclusief .mp4):"))
        layout.addWidget(self.output_input)
        layout.addWidget(self.run_button)
        self.setLayout(layout)

    def update_preview(self, effect_name):
        gif_path = f"previews/{effect_name}.gif"
        if os.path.exists(gif_path):
            self.preview.setPixmap(QPixmap(gif_path).scaled(240, 135, Qt.AspectRatioMode.KeepAspectRatio))

    def pick_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = color.name()

    def choose_bg_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.bg_color = color.name()
            self.bg_btn.setStyleSheet(f"background-color: {self.bg_color};")
            self.bg_btn = QPushButton("🌄 Kies achtergrondkleur")
            self.bg_btn.clicked.connect(self.choose_bg_color)     
            self.bg_color = "#000000"  # <- voeg deze regel toe

    def choose_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Kies video", "", "Video Files (*.mp4 *.mov *.avi)")
        if file:
            self.input_path = file
            self.file_button.setText(f"📂 {os.path.basename(file)}")

    def QLineEdit(self):
            self.output_input.setPlaceholderText("output_supervisual.mp4")
            self.output_input.text()


    def run_visual_engine(self):
        if not self.input_path: 
            print("⚠️ Geen inputbestand gekozen")
            return
        effect = self.effect_dropdown.currentText()
        fps = self.fps_slider.value()
        opacity = self.opacity_slider.value() / 100.0
        color = self.color
        bg_color = self.bg_color
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
        print("▶️ Running:", cmd)
        os.system(cmd)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = VisualizerGUI()
    gui.show()
    sys.exit(app.exec())
