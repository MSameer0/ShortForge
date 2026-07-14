from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QKeyEvent, QDragLeaveEvent
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
)

from utils.media import is_video
from widgets.empty_state import EmptyStateWidget
from widgets.playback_bar import PlaybackBar
from widgets.seek_slider import SeekSlider
from widgets.video_widget import VideoWidget


class PreviewWidget(QFrame):
    """
    Hosts the empty state, video player and playback controls.
    """

    openVideoRequested = Signal()

    # Emitted when a supported video is dropped.
    videoDropped = Signal(str)

    def __init__(self):
        super().__init__()

        self.setObjectName("previewFrame")

        self.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding,
        )

        self.setFocusPolicy(Qt.StrongFocus)
        self.setAcceptDrops(True)

        self._build_ui()
        self._connect_signals()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Title

        title = QLabel("Preview")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: 600;
        """)

        layout.addWidget(title)

        # Preview Area

        self.stack = QStackedWidget()

        self.empty = EmptyStateWidget()
        self.video = VideoWidget()

        self.stack.addWidget(self.empty)
        self.stack.addWidget(self.video)
        self.stack.setCurrentWidget(self.empty)

        layout.addWidget(self.stack, stretch=1)

        # Seek Slider

        self.slider = SeekSlider()
        self.slider.hide()

        layout.addWidget(self.slider)

        # Playback Controls

        self.controls = PlaybackBar()
        self.controls.hide()

        layout.addWidget(self.controls)

    def _connect_signals(self):
        # Empty State

        self.empty.openVideoRequested.connect(self.openVideoRequested.emit)

        # Playback Controls -> Video

        self.controls.playPauseRequested.connect(self.video.toggle_playback)

        self.controls.stopRequested.connect(self.video.stop)

        # Video -> Controls

        self.video.playbackStateChanged.connect(self.controls.on_playback_state_changed)

        self.video.positionChanged.connect(self._update_time)

        self.video.durationChanged.connect(self._update_time)

        # Video -> Slider

        self.video.durationChanged.connect(self.slider.setMaximum)

        self.video.positionChanged.connect(
            lambda pos: (
                self.slider.setValue(pos) if not self.slider.isSliderDown() else None
            )
        )

        # Slider -> Video

        self.slider.seekRequested.connect(self.video.set_position)

    def load_video(self, path: str):
        self.video.load(path)
        self.video.play()

        self.stack.setCurrentWidget(self.video)

        self.slider.show()
        self.controls.show()

        self.setFocus()

        self._update_time()

    def has_video(self) -> bool:
        return self.stack.currentWidget() is self.video

    def _update_time(self):
        self.controls.update_time(
            self.video.current_time_string(), self.video.duration_string()
        )

    # Keyboard Shortcuts

    def keyPressEvent(self, event: QKeyEvent):
        if not self.has_video():
            super().keyPressEvent(event)
            return

        key = event.key()

        if key == Qt.Key_Space:
            self.video.toggle_playback()

        elif key == Qt.Key_Left:
            self.video.seek_backward()

        elif key == Qt.Key_Right:
            self.video.seek_forward()

        elif key == Qt.Key_Home:
            self.video.set_position(0)

        elif key == Qt.Key_End:
            self.video.set_position(self.video.duration())

        else:
            super().keyPressEvent(event)

    # Drag & Drop

    def dragEnterEvent(self, event: QDragEnterEvent):
        mime = event.mimeData()

        if not mime.hasUrls():
            event.ignore()
            return

        urls = mime.urls()

        if len(urls) != 1:
            event.ignore()
            return

        path = urls[0].toLocalFile()

        if is_video(path):
            event.acceptProposedAction()
            self.set_drag_highlight(True)
        else:
            event.ignore()

    def dragLeaveEvent(self, event: QDragLeaveEvent):
        self.set_drag_highlight(False)
        event.accept()

    def dropEvent(self, event: QDropEvent):
        self.set_drag_highlight(False)
        urls = event.mimeData().urls()

        if not urls:
            return

        path = urls[0].toLocalFile()

        if is_video(path):
            self.videoDropped.emit(path)
            event.acceptProposedAction()
        else:
            event.ignore()

    def set_drag_highlight(self, enabled: bool):
        self.setProperty("dragging", enabled)

        self.style().unpolish(self)
        self.style().polish(self)

        self.update()
