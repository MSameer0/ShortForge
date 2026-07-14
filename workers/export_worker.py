from PySide6.QtCore import QThread, Signal
from video.encoder import export_short


class ExportWorker(QThread):
    """
    Background worker to run the FFmpeg export process without freezing the main UI thread.
    """

    # Emits (success, message)
    finished_export = Signal(bool, str)

    def __init__(self, output_path: str, parent=None):
        super().__init__(parent)
        self.output_path = output_path

    def run(self):
        try:
            export_short(self.output_path)
            self.finished_export.emit(True, "Video exported successfully!")
        except Exception as e:
            self.finished_export.emit(False, f"Export failed:\n{str(e)}")
