from dataclasses import dataclass
from PySide6.QtCore import QObject, Signal


@dataclass
class TextLayer:
    text: str
    start_ms: int
    end_ms: int
    font_size: int = 40
    color: str = "#FFFFFF"
    x_position_ratio: float = 0.5  # 0 to 1, relative to video width
    y_position_ratio: float = 0.5  # 0 to 1, relative to video height
    font_family: str = "Arial"
    stroke_color: str = "#000000"
    stroke_width: int = 3


class ProjectSettings(QObject):
    # Signals to notify UI and video player of state changes
    settingsChanged = Signal()
    trimChanged = Signal(int, int)  # start_ms, end_ms
    textLayersChanged = Signal()
    blurChanged = Signal(bool, int)  # enabled, intensity

    def __init__(self):
        super().__init__()
        self.video_path = ""
        self.video_duration_ms = 0

        self.trim_start_ms = 0
        self.trim_end_ms = 0

        self.blur_background = True
        self.blur_intensity = 30

        self.text_layers: list[TextLayer] = []

        # Actual pixel width of the 9:16 preview canvas — set by PreviewRenderer.
        # Used by the encoder to scale font sizes proportionally for 1080p export.
        self.preview_canvas_w: int = 300

    def set_video(self, path: str, duration_ms: int):
        self.video_path = path
        self.video_duration_ms = duration_ms
        self.trim_start_ms = 0
        self.trim_end_ms = duration_ms
        self.settingsChanged.emit()

    def set_trim(self, start_ms: int, end_ms: int):
        self.trim_start_ms = start_ms
        self.trim_end_ms = end_ms
        self.trimChanged.emit(start_ms, end_ms)
        self.settingsChanged.emit()

    def set_blur(self, enabled: bool, intensity: int):
        self.blur_background = enabled
        self.blur_intensity = intensity
        self.blurChanged.emit(enabled, intensity)
        self.settingsChanged.emit()

    def add_text_layer(self, layer: TextLayer):
        self.text_layers.append(layer)
        self.textLayersChanged.emit()
        self.settingsChanged.emit()

    def remove_text_layer(self, index: int):
        if 0 <= index < len(self.text_layers):
            self.text_layers.pop(index)
            self.textLayersChanged.emit()
            self.settingsChanged.emit()


# Global instance for the active project
active_project = ProjectSettings()
