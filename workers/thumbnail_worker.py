import cv2
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QImage, QPixmap


class ThumbnailWorker(QThread):
    """Background worker to extract evenly-spaced video frames as thumbnails."""

    # Emits the full list of pixmaps when done
    thumbnails_ready = Signal(list)

    def __init__(self, video_path: str, count: int, thumb_height: int, parent=None):
        super().__init__(parent)
        self.video_path = video_path
        self.count = max(count, 1)
        self.thumb_height = thumb_height
        self._cancelled = False

    def cancel(self):
        self._cancelled = True

    def run(self):
        pixmaps = []
        if not self.video_path:
            self.thumbnails_ready.emit(pixmaps)
            return

        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            self.thumbnails_ready.emit(pixmaps)
            return

        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        if fps <= 0 or total_frames <= 0:
            cap.release()
            self.thumbnails_ready.emit(pixmaps)
            return

        duration_ms = (total_frames / fps) * 1000.0
        step_ms = duration_ms / self.count

        for i in range(self.count):
            if self._cancelled:
                break

            cap.set(cv2.CAP_PROP_POS_MSEC, i * step_ms)
            ret, frame = cap.read()
            if not ret or frame is None:
                continue

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame_rgb.shape

            # Scale proportionally to target height
            thumb_w = max(1, int(w * (self.thumb_height / h)))
            frame_small = cv2.resize(
                frame_rgb, (thumb_w, self.thumb_height), interpolation=cv2.INTER_AREA
            )

            qimg = QImage(
                frame_small.data,
                thumb_w,
                self.thumb_height,
                ch * thumb_w,
                QImage.Format_RGB888,
            ).copy()
            pixmaps.append(QPixmap.fromImage(qimg))

        cap.release()
        if not self._cancelled:
            self.thumbnails_ready.emit(pixmaps)
