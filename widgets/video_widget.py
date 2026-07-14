from PySide6.QtCore import QUrl, Signal
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput, QVideoSink
from PySide6.QtWidgets import QWidget, QVBoxLayout

from video.preview_frame import PreviewRenderer
from utils.project import active_project


class VideoWidget(QWidget):
    """
    A reusable wrapper around Qt Multimedia.

    This widget is responsible only for loading and playing media.
    It intentionally hides the underlying QMediaPlayer from the rest
    of the application.
    """

    videoLoaded = Signal(str)

    def __init__(self):
        super().__init__()

        self._path = ""

        self._player = QMediaPlayer()
        self._audio = QAudioOutput()
        self._video_sink = QVideoSink()

        self._player.setAudioOutput(self._audio)
        self._player.setVideoSink(self._video_sink)

        self._renderer = PreviewRenderer()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._renderer)

        self._video_sink.videoFrameChanged.connect(self._renderer.set_frame)
        self._player.positionChanged.connect(self._renderer.set_position)

        self._player.durationChanged.connect(self._on_duration_changed)
        self._player.positionChanged.connect(self._enforce_trim_limits)

    # Expose Qt signals

    @property
    def positionChanged(self):
        return self._player.positionChanged

    @property
    def durationChanged(self):
        return self._player.durationChanged

    @property
    def playbackStateChanged(self):
        return self._player.playbackStateChanged

    # Media

    def load(self, path: str):
        self._path = path
        self._player.setSource(QUrl.fromLocalFile(path))
        self.videoLoaded.emit(path)

    def path(self) -> str:
        return self._path

    def play(self):
        # Always start from trim start if we are at the end or before trim start
        if (
            self.position() < active_project.trim_start_ms
            or self.position() >= active_project.trim_end_ms
        ):
            self.set_position(active_project.trim_start_ms)
        self._player.play()

    def pause(self):
        self._player.pause()

    def stop(self):
        self._player.stop()

    def toggle_playback(self):
        if self.is_playing():
            self.pause()
        else:
            self.play()

    def _on_duration_changed(self, duration: int):
        if duration > 0:
            active_project.set_video(self._path, duration)

    def _enforce_trim_limits(self, pos: int):
        if self.is_playing() and pos >= active_project.trim_end_ms:
            self.pause()
            self.set_position(active_project.trim_end_ms)

    # Position

    def position(self) -> int:
        return self._player.position()

    def duration(self) -> int:
        return self._player.duration()

    def set_position(self, ms: int):
        ms = max(0, min(ms, self.duration()))
        self._player.setPosition(ms)

    def seek_forward(self, ms: int = 5000):
        self.set_position(self.position() + ms)

    def seek_backward(self, ms: int = 5000):
        self.set_position(self.position() - ms)

    # Playback

    def is_playing(self) -> bool:
        return self._player.playbackState() == QMediaPlayer.PlayingState

    def set_volume(self, volume: float):
        volume = max(0.0, min(volume, 1.0))
        self._audio.setVolume(volume)

    # Helpers

    @staticmethod
    def format_time(ms: int) -> str:
        total_seconds = ms // 1000

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        if hours:
            return f"{hours:02}:{minutes:02}:{seconds:02}"

        return f"{minutes:02}:{seconds:02}"

    def current_time_string(self) -> str:
        return self.format_time(self.position())

    def duration_string(self) -> str:
        return self.format_time(self.duration())
