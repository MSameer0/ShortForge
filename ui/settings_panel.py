from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QCheckBox,
    QSlider,
    QPushButton,
    QHBoxLayout,
    QScrollArea,
    QFrame,
    QInputDialog,
    QColorDialog,
    QFileDialog,
    QMessageBox,
)

from utils.project import active_project, TextLayer
from video.encoder import export_short


def _divider():
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setFixedHeight(1)
    line.setObjectName("settingsDivider")
    return line


def _section_title(text):
    label = QLabel(text)
    label.setStyleSheet(
        "font-size: 11pt; font-weight: 600; color: #E4E4E7;"
        "background: transparent; border: none; padding: 0;"
    )
    return label


def _format_time(ms):
    s = ms // 1000
    m, s = divmod(s, 60)
    return f"{m}:{s:02d}"


class SettingsPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("settingsPanel")
        self.setMinimumWidth(250)

        self._build_ui()
        self._connect_signals()
        self._sync_ui_to_state()

    def _build_ui(self):
        from ui.project_settings_dialog import ProjectSettingsDialog
        self.ProjectSettingsDialog = ProjectSettingsDialog
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(12)

        top_btns = QHBoxLayout()
        self.btn_proj_settings = QPushButton("⚙️ Settings")
        self.btn_proj_settings.setCursor(Qt.PointingHandCursor)
        self.btn_export = QPushButton("Export Video")
        self.btn_export.setObjectName("exportButton")
        self.btn_export.setCursor(Qt.PointingHandCursor)
        
        top_btns.addWidget(self.btn_proj_settings)
        top_btns.addWidget(self.btn_export, stretch=1)
        layout.addLayout(top_btns)

        layout.addWidget(_divider())

        layout.addWidget(_section_title("Background"))

        self.chk_blur = QCheckBox("Blur Background")
        self.chk_blur.setChecked(True)
        layout.addWidget(self.chk_blur)

        slider_row = QHBoxLayout()
        slider_row.setSpacing(8)
        slider_label = QLabel("Intensity")
        slider_label.setStyleSheet(
            "color: #A1A1AA; border: none; background: transparent;"
        )
        self.slider_intensity = QSlider(Qt.Horizontal)
        self.slider_intensity.setRange(1, 100)
        self.slider_intensity.setValue(30)
        self.lbl_intensity_value = QLabel("30")
        self.lbl_intensity_value.setFixedWidth(28)
        self.lbl_intensity_value.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.lbl_intensity_value.setStyleSheet(
            "color: #A1A1AA; border: none; background: transparent;"
        )
        slider_row.addWidget(slider_label)
        slider_row.addWidget(self.slider_intensity, 1)
        slider_row.addWidget(self.lbl_intensity_value)
        layout.addLayout(slider_row)

        layout.addWidget(_divider())

        text_header = QHBoxLayout()
        text_header.addWidget(_section_title("Text Layers"))
        text_header.addStretch()
        self.btn_add_text = QPushButton("+")
        self.btn_add_text.setFixedSize(28, 28)
        self.btn_add_text.setCursor(Qt.PointingHandCursor)
        self.btn_add_text.setStyleSheet(
            "QPushButton { font-size: 14pt; font-weight: bold; padding: 0;"
            "border-radius: 6px; }"
        )
        text_header.addWidget(self.btn_add_text)
        layout.addLayout(text_header)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet(
            "QScrollArea { background: transparent; border: none; }"
        )
        self.text_list_widget = QWidget()
        self.text_list_widget.setStyleSheet("background: transparent; border: none;")
        self.text_list_layout = QVBoxLayout(self.text_list_widget)
        self.text_list_layout.setContentsMargins(0, 0, 0, 0)
        self.text_list_layout.setSpacing(6)
        self.text_list_layout.setAlignment(Qt.AlignTop)
        self.scroll_area.setWidget(self.text_list_widget)
        layout.addWidget(self.scroll_area, stretch=1)

    def _connect_signals(self):
        self.btn_proj_settings.clicked.connect(self._on_proj_settings_clicked)
        self.btn_export.clicked.connect(self._on_export_clicked)
        self.chk_blur.stateChanged.connect(self._on_blur_changed)
        self.slider_intensity.valueChanged.connect(self._on_blur_changed)
        self.slider_intensity.valueChanged.connect(
            lambda v: self.lbl_intensity_value.setText(str(v))
        )
        self.btn_add_text.clicked.connect(self._on_add_text_clicked)
        active_project.textLayersChanged.connect(self._update_text_layers_ui)

    def _on_proj_settings_clicked(self):
        dialog = self.ProjectSettingsDialog(self)
        dialog.exec()

    def _sync_ui_to_state(self):
        self.chk_blur.setChecked(active_project.blur_background)
        self.slider_intensity.setValue(active_project.blur_intensity)
        self._update_text_layers_ui()

    def _on_blur_changed(self):
        active_project.set_blur(
            self.chk_blur.isChecked(), self.slider_intensity.value()
        )

    def _on_add_text_clicked(self):
        from ui.text_layer_dialog import TextLayerDialog

        dialog = TextLayerDialog(
            self,
            start_ms=active_project.trim_start_ms,
            end_ms=active_project.trim_end_ms,
        )
        if dialog.exec():
            active_project.add_text_layer(dialog.get_layer())

    def _update_text_layers_ui(self):
        while self.text_list_layout.count():
            item = self.text_list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for i, layer in enumerate(active_project.text_layers):
            card = QFrame()
            card.setObjectName("textLayerCard")
            card_layout = QHBoxLayout(card)
            card_layout.setContentsMargins(10, 8, 8, 8)
            card_layout.setSpacing(8)

            info = QVBoxLayout()
            info.setSpacing(2)

            text_label = QLabel(layer.text)
            text_label.setStyleSheet(
                "color: #E4E4E7; font-size: 10pt; font-weight: 500;"
                "background: transparent; border: none;"
            )
            text_label.setWordWrap(True)

            time_label = QLabel(
                f"{_format_time(layer.start_ms)} – {_format_time(layer.end_ms)}"
            )
            time_label.setStyleSheet(
                "color: #71717A; font-size: 8.5pt;"
                "background: transparent; border: none;"
            )

            info.addWidget(text_label)
            info.addWidget(time_label)
            card_layout.addLayout(info, 1)

            btn_edit = QPushButton("✎")
            btn_edit.setFixedSize(24, 24)
            btn_edit.setCursor(Qt.PointingHandCursor)
            btn_edit.setStyleSheet(
                "QPushButton { background: transparent; border: none;"
                "color: #A1A1AA; font-size: 11pt; border-radius: 4px; padding: 0; }"
                "QPushButton:hover { color: #FFFFFF; background-color: #3F3F46; }"
            )

            def make_edit_handler(l=layer):
                def handler():
                    from ui.text_layer_dialog import TextLayerDialog

                    dialog = TextLayerDialog(self, layer=l)
                    if dialog.exec():
                        dialog.get_layer()  # This actually mutates the layer
                        active_project.textLayersChanged.emit()
                        active_project.settingsChanged.emit()

                return handler

            btn_edit.clicked.connect(make_edit_handler())

            btn_del = QPushButton("✕")
            btn_del.setFixedSize(24, 24)
            btn_del.setCursor(Qt.PointingHandCursor)
            btn_del.setStyleSheet(
                "QPushButton { background: transparent; border: none;"
                "color: #52525B; font-size: 11pt; border-radius: 4px; padding: 0; }"
                "QPushButton:hover { color: #EF4444; background-color: #1a1014; }"
            )
            btn_del.clicked.connect(
                lambda checked, idx=i: active_project.remove_text_layer(idx)
            )
            card_layout.addWidget(btn_edit, 0, Qt.AlignTop)
            card_layout.addWidget(btn_del, 0, Qt.AlignTop)

            self.text_list_layout.addWidget(card)

    def _on_export_clicked(self):
        if not active_project.video_path:
            QMessageBox.warning(self, "Export", "No video loaded.")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Short", "", "Video Files (*.mp4)"
        )

        if file_path:
            from PySide6.QtWidgets import QProgressDialog
            from workers.export_worker import ExportWorker

            self.progress = QProgressDialog(
                "Exporting video... This may take a few minutes.", "Cancel", 0, 0, self
            )
            self.progress.setWindowTitle("Exporting")
            self.progress.setWindowModality(Qt.WindowModal)
            self.progress.setCancelButton(None)  # disable cancel for now

            self.worker = ExportWorker(file_path, self)

            def on_finished(success, msg):
                self.progress.close()
                if success:
                    QMessageBox.information(self, "Export Complete", msg)
                else:
                    QMessageBox.critical(self, "Export Failed", msg)

            self.worker.finished_export.connect(on_finished)
            self.worker.start()
            self.progress.exec()
