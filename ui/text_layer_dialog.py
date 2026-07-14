from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QColorDialog,
    QSpinBox,
)

from utils.project import TextLayer
from widgets.font_combo import FontComboBox


class TextLayerDialog(QDialog):
    """
    Dialog for adding or editing a TextLayer.
    """

    def __init__(
        self, parent=None, layer: TextLayer = None, start_ms: int = 0, end_ms: int = 0
    ):
        super().__init__(parent)
        self.setWindowTitle("Edit Text Layer" if layer else "Add Text Layer")
        self.setMinimumWidth(400)
        self.setModal(True)

        self.layer = layer
        self.start_ms = start_ms if not layer else layer.start_ms
        self.end_ms = end_ms if not layer else layer.end_ms

        self.text_color = QColor(layer.color if layer else "#FFFFFF")
        self.stroke_color = QColor(layer.stroke_color if layer else "#000000")

        self._build_ui()
        if layer:
            self._populate()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        self.txt_input = QLineEdit()
        self.txt_input.setPlaceholderText("Enter text here...")
        layout.addWidget(QLabel("Text:"))
        layout.addWidget(self.txt_input)

        font_layout = QHBoxLayout()
        self.font_combo = FontComboBox()
        self.font_combo.setMaxVisibleItems(15)
        font_layout.addWidget(QLabel("Font:"))
        font_layout.addWidget(self.font_combo, 1)
        layout.addLayout(font_layout)

        color_layout = QHBoxLayout()
        self.btn_text_color = QPushButton("Text Color")
        self.btn_text_color.setStyleSheet(
            f"background-color: {self.text_color.name()}; color: {'#000' if self.text_color.lightness() > 128 else '#FFF'};"
        )
        self.btn_text_color.clicked.connect(self._pick_text_color)

        self.btn_stroke_color = QPushButton("Stroke Color")
        self.btn_stroke_color.setStyleSheet(
            f"background-color: {self.stroke_color.name()}; color: {'#000' if self.stroke_color.lightness() > 128 else '#FFF'};"
        )
        self.btn_stroke_color.clicked.connect(self._pick_stroke_color)

        color_layout.addWidget(self.btn_text_color)
        color_layout.addWidget(self.btn_stroke_color)
        layout.addLayout(color_layout)

        stroke_layout = QHBoxLayout()
        self.spin_stroke_width = QSpinBox()
        self.spin_stroke_width.setRange(0, 20)
        self.spin_stroke_width.setValue(3)
        stroke_layout.addWidget(QLabel("Stroke Width:"))
        stroke_layout.addWidget(self.spin_stroke_width)
        stroke_layout.addStretch()
        layout.addLayout(stroke_layout)

        size_layout = QHBoxLayout()
        self.spin_font_size = QSpinBox()
        self.spin_font_size.setRange(10, 200)
        self.spin_font_size.setValue(40)
        size_layout.addWidget(QLabel("Font Size:"))
        size_layout.addWidget(self.spin_font_size)
        size_layout.addStretch()
        layout.addLayout(size_layout)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_cancel = QPushButton("Cancel")
        btn_cancel.clicked.connect(self.reject)
        self.btn_save = QPushButton("Save")
        self.btn_save.setDefault(True)
        self.btn_save.clicked.connect(self.accept)

        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(self.btn_save)
        layout.addLayout(btn_layout)

    def _populate(self):
        self.txt_input.setText(self.layer.text)
        self.font_combo.setCurrentFontFamily(self.layer.font_family)
        self.spin_stroke_width.setValue(self.layer.stroke_width)
        self.spin_font_size.setValue(self.layer.font_size)

    def _pick_text_color(self):
        color = QColorDialog.getColor(self.text_color, self, "Select Text Color")
        if color.isValid():
            self.text_color = color
            self.btn_text_color.setStyleSheet(
                f"background-color: {self.text_color.name()}; color: {'#000' if self.text_color.lightness() > 128 else '#FFF'};"
            )

    def _pick_stroke_color(self):
        color = QColorDialog.getColor(self.stroke_color, self, "Select Stroke Color")
        if color.isValid():
            self.stroke_color = color
            self.btn_stroke_color.setStyleSheet(
                f"background-color: {self.stroke_color.name()}; color: {'#000' if self.stroke_color.lightness() > 128 else '#FFF'};"
            )

    def get_layer(self) -> TextLayer:
        """Returns the configured TextLayer."""
        text = self.txt_input.text().strip() or "Text"

        if self.layer:
            # Update existing
            self.layer.text = text
            self.layer.font_family = self.font_combo.currentFontFamily()
            self.layer.color = self.text_color.name()
            self.layer.stroke_color = self.stroke_color.name()
            self.layer.stroke_width = self.spin_stroke_width.value()
            self.layer.font_size = self.spin_font_size.value()
            return self.layer
        else:
            # Create new
            return TextLayer(
                text=text,
                start_ms=self.start_ms,
                end_ms=self.end_ms,
                font_size=self.spin_font_size.value(),
                color=self.text_color.name(),
                font_family=self.font_combo.currentFontFamily(),
                stroke_color=self.stroke_color.name(),
                stroke_width=self.spin_stroke_width.value(),
            )
