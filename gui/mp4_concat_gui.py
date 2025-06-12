import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QTextEdit
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import subprocess

class MP4ConcatThread(QThread):
    progress_signal = pyqtSignal(int)
    max_progress_signal = pyqtSignal(int)
    done_signal = pyqtSignal(bool, str)

    def __init__(self, cmd, total_files):
        super().__init__()
        self.cmd = cmd
        self.total_files = total_files

    def run(self):
        # Simulate progress: 0% at start, 100% at end
        self.max_progress_signal.emit(self.total_files)
        self.progress_signal.emit(0)
        try:
            subprocess.run(self.cmd, check=True, capture_output=True, text=True)
            self.progress_signal.emit(self.total_files)
            self.done_signal.emit(True, "✅ Samengevoegd")
        except subprocess.CalledProcessError as e:
            self.done_signal.emit(False, f"❌ Fout:\n{e.stderr}")

class MP4ConcatGUI(QWidget):
    thread_created = pyqtSignal(QThread)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MP4 Plakker")
        self.setMinimumSize(350, 180)
        layout = QVBoxLayout()

        self.files = []
        self.select_btn = QPushButton("📂 Kies MP4 bestanden (in volgorde)")
        self.select_btn.clicked.connect(self.choose_files)
        layout.addWidget(self.select_btn)

        self.label = QLabel("Geen bestanden gekozen.")
        layout.addWidget(self.label)

        self.concat_btn = QPushButton("▶️ Plak samen en exporteer")
        self.concat_btn.clicked.connect(self.concat_files)
        self.concat_btn.setEnabled(False)
        layout.addWidget(self.concat_btn)

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setMinimumHeight(40)
        layout.addWidget(self.console)

        self.setLayout(layout)

    def choose_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Kies MP4 bestanden", "", "MP4 Files (*.mp4)")
        if files:
            self.files = files
            self.label.setText("\n".join([f"{i+1}. {f}" for i, f in enumerate(files)]))
            self.concat_btn.setEnabled(True)
        else:
            self.label.setText("Geen bestanden gekozen.")
            self.concat_btn.setEnabled(False)

    def concat_files(self):
        if not self.files:
            self.console.setPlainText("⚠️ Geen bestanden gekozen.")
            return
        out_file, _ = QFileDialog.getSaveFileName(self, "Opslaan als", "output_concat.mp4", "MP4 Files (*.mp4)")
        if not out_file:
            return
        # Maak tijdelijke lijstfile voor ffmpeg
        import tempfile
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            for file in self.files:
                f.write(f"file '{file}'\n")
            listfile = f.name
        cmd = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listfile, "-c", "copy", out_file
        ]
        self.console.setPlainText(f"▶️ Running: {' '.join(cmd)}")
        self.thread = MP4ConcatThread(cmd, len(self.files))
        self.thread.progress_signal.connect(self.update_progress)
        self.thread.max_progress_signal.connect(self.set_progress_max)
        self.thread_created.emit(self.thread)
        def on_done(success, msg):
            self.console.append(msg)
        self.thread.done_signal.connect(on_done)
        self.thread.start()

    def update_progress(self, value):
        pass

    def set_progress_max(self, value):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = MP4ConcatGUI()
    gui.show()
    sys.exit(app.exec())
