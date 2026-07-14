from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QSlider


class SeekSlider(QSlider):
    """
    Slider used to seek through the currently loaded media.

    Unlike a normal QSlider, clicking anywhere on the bar jumps
    directly to that position.
    """

    seekRequested = Signal(int)

    def __init__(self):
        super().__init__(Qt.Horizontal)

        self.setRange(0, 0)

        self.sliderMoved.connect(self.seekRequested.emit)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            value = self.minimum() + (
                (self.maximum() - self.minimum()) * event.position().x() / self.width()
            )

            self.setValue(int(value))
            self.seekRequested.emit(self.value())

        super().mousePressEvent(event)
