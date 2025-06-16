# vem_visualizer.py
import sys
import numpy as np
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider
from PyQt6.QtCore import QTimer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from scipy.ndimage import gaussian_filter

def generate_frame(t, freq=5, size=(256, 256)):
    x = np.linspace(-3, 3, size[1])
    y = np.linspace(-3, 3, size[0])
    X, Y = np.meshgrid(x, y)

    base = np.sin(freq * np.sqrt(X**2 + Y**2) - t * 0.2)
    transition = np.tanh(np.sin(2 * X + t * 0.1) * np.cos(2 * Y - t * 0.1))
    combined = base * transition
    return gaussian_filter(combined, sigma=1.0)

class FeedbackVisualizer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("v.E.M. Feedback Synth")
        self.t = 0
        self.freq = 5

        # UI setup
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.ax.axis('off')
        self.img = self.ax.imshow(generate_frame(self.t, self.freq), cmap='magma', animated=True)

        self.slider = QSlider()
        self.slider.setMinimum(1)
        self.slider.setMaximum(20)
        self.slider.setValue(self.freq)
        self.slider.valueChanged.connect(self.on_slider)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.slider)
        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(50)

    def on_slider(self, value):
        self.freq = value

    def update_frame(self):
        self.t += 1
        frame = generate_frame(self.t, self.freq)
        self.img.set_array(frame)
        self.canvas.draw_idle()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = FeedbackVisualizer()
    win.show()
    sys.exit(app.exec())