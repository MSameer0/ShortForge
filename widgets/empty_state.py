from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class EmptyStateWidget(QWidget):
    openVideoRequested = Signal()

    def __init__(self):
        super().__init__()
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(12)

        icon = QLabel("🎬")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setStyleSheet(
            "font-size: 48px;" "background: transparent;" "border: none;"
        )

        title = QLabel("No Video Loaded")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            "font-size: 22px;"
            "font-weight: 700;"
            "color: #E4E4E7;"
            "background: transparent;"
            "border: none;"
            "letter-spacing: 0.5px;"
        )

        subtitle = QLabel(
            "Drag & drop a video here\n" "or double-click anywhere to browse."
        )
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet(
            "color: #71717A;"
            "font-size: 12px;"
            "line-height: 1.5;"
            "background: transparent;"
            "border: none;"
        )

        button = QPushButton("Open Video")
        button.setFixedWidth(180)
        button.setCursor(Qt.PointingHandCursor)
        button.setStyleSheet(
            "QPushButton {"
            "  background-color: #8B5CF6;"
            "  border: none;"
            "  border-radius: 8px;"
            "  padding: 10px 24px;"
            "  color: #FFFFFF;"
            "  font-size: 11pt;"
            "  font-weight: 600;"
            "}"
            "QPushButton:hover {"
            "  background-color: #7C3AED;"
            "}"
            "QPushButton:pressed {"
            "  background-color: #6D28D9;"
            "}"
        )
        button.clicked.connect(self.openVideoRequested.emit)

        layout.addWidget(icon)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(8)
        layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.openVideoRequested.emit()
            event.accept()
            return

        super().mouseDoubleClickEvent(event)
