from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
)
from PySide6.QtGui import QIntValidator

from utils.project import active_project


class ProjectSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Project Settings")
        self.setFixedWidth(300)
        self.setModal(True)

        self._build_ui()
        self._populate_fields()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        # Width
        w_layout = QHBoxLayout()
        w_label = QLabel("Export Width:")
        self.w_input = QLineEdit()
        self.w_input.setValidator(QIntValidator(1, 8192))
        w_layout.addWidget(w_label)
        w_layout.addWidget(self.w_input)
        layout.addLayout(w_layout)

        # Height
        h_layout = QHBoxLayout()
        h_label = QLabel("Export Height:")
        self.h_input = QLineEdit()
        self.h_input.setValidator(QIntValidator(1, 8192))
        h_layout.addWidget(h_label)
        h_layout.addWidget(self.h_input)
        layout.addLayout(h_layout)

        # FPS
        fps_layout = QHBoxLayout()
        fps_label = QLabel("Export FPS:")
        self.fps_input = QLineEdit()
        self.fps_input.setValidator(QIntValidator(1, 240))
        fps_layout.addWidget(fps_label)
        fps_layout.addWidget(self.fps_input)
        layout.addLayout(fps_layout)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        cancel_btn = QPushButton("Cancel")
        save_btn = QPushButton("Save")
        save_btn.setDefault(True)

        cancel_btn.clicked.connect(self.reject)
        save_btn.clicked.connect(self._save_settings)

        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)

    def _populate_fields(self):
        self.w_input.setText(str(active_project.export_width))
        self.h_input.setText(str(active_project.export_height))
        self.fps_input.setText(str(active_project.export_fps))

    def _save_settings(self):
        try:
            w = int(self.w_input.text())
            h = int(self.h_input.text())
            fps = int(self.fps_input.text())
            
            # Ensure safe constraints
            w = max(100, min(8192, w))
            h = max(100, min(8192, h))
            fps = max(1, min(240, fps))
            
            # Adjust to even dimensions (FFmpeg requires even numbers for H.264)
            if w % 2 != 0: w -= 1
            if h % 2 != 0: h -= 1

            active_project.set_export_settings(w, h, fps)
            self.accept()
        except ValueError:
            pass
