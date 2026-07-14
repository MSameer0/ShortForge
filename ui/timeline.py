from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QHBoxLayout
from widgets.range_slider import RangeSlider
from utils.project import active_project


class TimelineWidget(QFrame):
    def __init__(self):
        super().__init__()

        self.setObjectName("timelineFrame")
        self.setMinimumHeight(100)

        self._thumb_worker = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 12, 20, 12)

        title = QLabel("Timeline (Trim)")
        title.setStyleSheet("""
            font-size:16px;
            font-weight:600;
        """)

        self.range_slider = RangeSlider()

        self.time_label = QLabel("00:00 / 00:00")
        self.time_label.setStyleSheet("color:#AAAAAA;")

        header_layout = QHBoxLayout()
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.time_label)

        layout.addLayout(header_layout)
        layout.addStretch()
        layout.addWidget(self.range_slider)
        layout.addStretch()

        self.range_slider.rangeChanged.connect(self._on_slider_changed)
        active_project.settingsChanged.connect(self._sync_with_project)

    def _on_slider_changed(self, low, high):
        active_project.set_trim(low, high)
        self._update_time_label(low, high)

    def _sync_with_project(self):
        self.range_slider.setMaximum(active_project.video_duration_ms)

        if active_project.trim_end_ms == 0 and active_project.video_duration_ms > 0:
            # Initial load or full duration
            active_project.set_trim(0, active_project.video_duration_ms)

        self.range_slider.setLow(active_project.trim_start_ms)
        self.range_slider.setHigh(active_project.trim_end_ms)
        self._update_time_label(
            active_project.trim_start_ms, active_project.trim_end_ms
        )

        # Generate thumbnails when a video is loaded
        if active_project.video_path:
            self._generate_thumbnails()

    def _generate_thumbnails(self):
        # Cancel any previous worker
        if self._thumb_worker and self._thumb_worker.isRunning():
            self._thumb_worker.cancel()
            self._thumb_worker.wait()

        from workers.thumbnail_worker import ThumbnailWorker

        # Calculate how many thumbnails to extract based on slider width
        slider_w = self.range_slider.width()
        thumb_h = self.range_slider.thumbnail_strip_height()
        # Each thumbnail tile is roughly 16:9, so tile width ≈ thumb_h * 16/9
        tile_w = max(1, int(thumb_h * 16 / 9))
        count = max(4, slider_w // tile_w)

        self._thumb_worker = ThumbnailWorker(
            active_project.video_path, count, thumb_h, self
        )
        self._thumb_worker.thumbnails_ready.connect(self._on_thumbnails_ready)
        self._thumb_worker.start()

    def _on_thumbnails_ready(self, pixmaps):
        self.range_slider.set_thumbnails(pixmaps)

    def _update_time_label(self, low, high):
        def format_time(ms: int) -> str:
            s = ms // 1000
            m = s // 60
            s = s % 60
            return f"{m:02}:{s:02}"

        self.time_label.setText(f"{format_time(low)} - {format_time(high)}")
