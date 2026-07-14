from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QStyle,
)
from PySide6.QtMultimedia import QMediaPlayer


class PlaybackBar(QWidget):
    """
    Playback controls displayed beneath the video preview.
    """

    playPauseRequested = Signal()
    stopRequested = Signal()

    def __init__(self):
        super().__init__()

        self._is_playing = False

        self._build_ui()

    def _build_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(10)

        self.play_button = QPushButton()
        self.play_button.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay)
        )
        self.play_button.setFixedSize(36, 36)

        self.stop_button = QPushButton()
        self.stop_button.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_MediaStop)
        )
        self.stop_button.setFixedSize(36, 36)

        self.time_label = QLabel("00:00 / 00:00")
        self.time_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        layout.addWidget(self.play_button)
        layout.addWidget(self.stop_button)
        layout.addStretch()
        layout.addWidget(self.time_label)

        self.play_button.clicked.connect(self.playPauseRequested.emit)

        self.stop_button.clicked.connect(self.stopRequested.emit)

    def set_playing(self, playing: bool):
        """
        Updates the play button icon.
        """

        self._is_playing = playing

        icon = (
            QStyle.StandardPixmap.SP_MediaPause
            if playing
            else QStyle.StandardPixmap.SP_MediaPlay
        )

        self.play_button.setIcon(self.style().standardIcon(icon))

    def update_time(self, current: str, total: str):
        self.time_label.setText(f"{current} / {total}")

    def on_playback_state_changed(self, state):
        """
        Convenience slot that can be connected directly to
        VideoWidget.playbackStateChanged.
        """

        self.set_playing(state == QMediaPlayer.PlaybackState.PlayingState)
