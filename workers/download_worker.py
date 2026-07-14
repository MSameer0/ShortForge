"""
Worker thread for downloading videos from URLs using yt-dlp.
Supports YouTube links and direct video URLs.
"""

import os
import tempfile
from PySide6.QtCore import QThread, Signal


class DownloadWorker(QThread):
    """
    Downloads a video from a URL using yt-dlp.
    Emits progress and completion signals.
    """

    progress = Signal(str)  # status message
    finished = Signal(str)  # downloaded file path
    error = Signal(str)  # error message

    def __init__(self, url: str, output_dir: str = None):
        super().__init__()
        self.url = url.strip()
        self.output_dir = output_dir or tempfile.mkdtemp(prefix="shortforge_")
        self._output_path = ""

    def run(self):
        try:
            import yt_dlp
        except ImportError:
            self.error.emit(
                "yt-dlp is not installed.\n" "Install it with:  pip install yt-dlp"
            )
            return

        output_template = os.path.join(self.output_dir, "%(title).80s.%(ext)s")

        ydl_opts = {
            "format": "b[ext=mp4]/b",
            "outtmpl": output_template,
            "quiet": True,
            "no_warnings": True,
            "progress_hooks": [self._on_progress],
        }

        try:
            self.progress.emit("Connecting...")

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=True)
                filename = ydl.prepare_filename(info)

                # yt-dlp may change the extension after merging
                if not os.path.isfile(filename):
                    base, _ = os.path.splitext(filename)
                    filename = base + ".mp4"

                self._output_path = filename
                self.finished.emit(filename)

        except Exception as exc:
            self.error.emit(str(exc))

    def _on_progress(self, d: dict):
        if d.get("status") == "downloading":
            pct = d.get("_percent_str", "?%").strip()
            speed = d.get("_speed_str", "").strip()
            self.progress.emit(f"Downloading: {pct}  {speed}")
        elif d.get("status") == "finished":
            self.progress.emit("Merging...")
