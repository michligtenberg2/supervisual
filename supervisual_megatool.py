import sys
from PyQt6.QtWidgets import QApplication, QTabWidget, QVBoxLayout, QWidget, QProgressBar, QTextEdit
from PyQt6.QtCore import Qt

# Import your existing GUIs
from video_effect_gui import VideoEffectGUI
from photo_spectrogram_gui import PhotoSpectroGUI
from preview_mp4_gui import PreviewMP4GUI
from mp4_concat_gui import MP4ConcatGUI

class SupervisualMegaTool(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Supervisual MegaTool Suite")
        self.setMinimumSize(650, 500)

        # Add each tool as a tab
        self.video_tab = VideoEffectGUI()
        self.photo_tab = PhotoSpectroGUI()
        self.preview_tab = PreviewMP4GUI()
        self.concat_tab = MP4ConcatGUI()
        self.addTab(self.video_tab, "Video Effect")
        self.addTab(self.photo_tab, "Photo Spectrogram")
        self.addTab(self.preview_tab, "MP4 Preview")
        self.addTab(self.concat_tab, "MP4 Concatenation")

        # Add a global log and progress bar at the bottom
        log_layout = QVBoxLayout()
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMinimumHeight(40)
        log_layout.addWidget(self.log_text)
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        log_layout.addWidget(self.progress_bar)
        # Remove log_widget and use log_layout directly

        # Add the log/progress bar below the tabs
        main_layout = QVBoxLayout()
        main_layout.addWidget(self)
        log_container = QWidget()
        log_container.setLayout(log_layout)
        main_layout.addWidget(log_container)
        container = QWidget()
        container.setLayout(main_layout)
        self.main_window = container

        # Connect signals from each tab to update the log and progress bar
        self._connect_tab_signals(self.video_tab)
        self._connect_tab_signals(self.photo_tab)
        self._connect_tab_signals(self.preview_tab)
        self._connect_tab_signals(self.concat_tab)
        # Listen for new threads created in tabs
        if hasattr(self.video_tab, 'thread_created'):
            self.video_tab.thread_created.connect(self._connect_thread_signals)
        if hasattr(self.photo_tab, 'thread_created'):
            self.photo_tab.thread_created.connect(self._connect_thread_signals)
        if hasattr(self.preview_tab, 'thread_created'):
            self.preview_tab.thread_created.connect(self._connect_thread_signals)
        if hasattr(self.concat_tab, 'thread_created'):
            self.concat_tab.thread_created.connect(self._connect_thread_signals)

    def _connect_tab_signals(self, tab):
        # Try to connect log_signal and progress_signal if present (legacy, for first thread)
        if hasattr(tab, 'thread') and hasattr(tab.thread, 'log_signal'):
            tab.thread.log_signal.connect(self.append_log)
        if hasattr(tab, 'thread') and hasattr(tab.thread, 'progress_signal'):
            tab.thread.progress_signal.connect(self.update_progress)
        if hasattr(tab, 'thread') and hasattr(tab.thread, 'max_progress_signal'):
            tab.thread.max_progress_signal.connect(self.set_progress_max)

    def _connect_thread_signals(self, thread):
        # Only connect progress for concat_tab (no log)
        if hasattr(thread, 'progress_signal'):
            thread.progress_signal.connect(self.update_progress)
        if hasattr(thread, 'max_progress_signal'):
            thread.max_progress_signal.connect(self.set_progress_max)
        # For other tabs, also connect log_signal
        if hasattr(thread, 'log_signal') and not isinstance(thread, type(self.concat_tab)):
            thread.log_signal.connect(self.append_log)

    def set_progress_max(self, value):
        self.progress_bar.setMaximum(value)

    def append_log(self, msg):
        self.log_text.append(msg)
        self.log_text.verticalScrollBar().setValue(self.log_text.verticalScrollBar().maximum())

    def update_progress(self, value):
        self.progress_bar.setValue(value)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mega_tabs = SupervisualMegaTool()
    main_window = mega_tabs.main_window
    main_window.setWindowTitle("Supervisual MegaTool Suite")
    main_window.setMinimumSize(650, 600)
    main_window.show()
    sys.exit(app.exec())
