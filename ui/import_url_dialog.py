"""
Dialog for importing videos from YouTube or direct video URLs.
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QProgressBar,
)

from workers.download_worker import DownloadWorker


class ImportUrlDialog(QDialog):
    """
    A dialog that lets the user paste a YouTube or direct video URL,
    downloads it via yt-dlp, and emits the local file path on success.
    """

    videoReady = Signal(str)  # path to downloaded file

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Import from URL")
        self.setMinimumWidth(500)
        self.setModal(True)

        self._worker = None
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Title
        title = QLabel("Import Video from URL")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("Paste a YouTube link or a direct video URL below.")
        subtitle.setStyleSheet("color: #A1A1AA; font-size: 12px;")
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        # URL input
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText(
            "https://www.youtube.com/watch?v=... or https://example.com/video.mp4"
        )
        self.url_input.setMinimumHeight(36)
        layout.addWidget(self.url_input)

        # Progress
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #A1A1AA;")
        layout.addWidget(self.status_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # indeterminate
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.clicked.connect(self._on_cancel)

        self.btn_import = QPushButton("Import")
        self.btn_import.setObjectName("exportButton")
        self.btn_import.clicked.connect(self._on_import)

        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_import)
        layout.addLayout(btn_layout)

    # Actions

    def _on_import(self):
        url = self.url_input.text().strip()
        if not url:
            self.status_label.setText("Please enter a URL.")
            return

        self.btn_import.setEnabled(False)
        self.url_input.setEnabled(False)
        self.progress_bar.show()
        self.status_label.setText("Starting download...")

        self._worker = DownloadWorker(url)
        self._worker.progress.connect(self._on_progress)
        self._worker.finished.connect(self._on_finished)
        self._worker.error.connect(self._on_error)
        self._worker.start()

    def _on_cancel(self):
        if self._worker and self._worker.isRunning():
            self._worker.terminate()
            self._worker.wait(3000)
        self.reject()

    # Slots

    def _on_progress(self, msg: str):
        self.status_label.setText(msg)

    def _on_finished(self, path: str):
        self.progress_bar.hide()
        self.status_label.setText(f"Downloaded: {path}")
        self.videoReady.emit(path)
        self.accept()

    def _on_error(self, msg: str):
        self.progress_bar.hide()
        self.btn_import.setEnabled(True)
        self.url_input.setEnabled(True)
        self.status_label.setText(f"Error: {msg}")
        self.status_label.setStyleSheet("color: #EF4444;")
