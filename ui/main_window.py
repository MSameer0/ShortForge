from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QDockWidget,
)

from ui.about_dialogue import AboutDialogue
from ui.import_url_dialog import ImportUrlDialog
from ui.menu_bar import MenuBar
from ui.preview import PreviewWidget
from ui.timeline import TimelineWidget

from utils.app_info import APP_NAME
from utils.constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    MIN_WINDOW_WIDTH,
    MIN_WINDOW_HEIGHT,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(APP_NAME)

        self.resize(
            WINDOW_WIDTH,
            WINDOW_HEIGHT,
        )

        self.setMinimumSize(
            MIN_WINDOW_WIDTH,
            MIN_WINDOW_HEIGHT,
        )

        # Allow nested docking so panels can be stacked/tabbed
        self.setDockNestingEnabled(True)

        self._build_ui()
        self._build_menu()
        self._connect_signals()

    def _build_ui(self):
        # Preview is the central widget (always docked)
        self.preview = PreviewWidget()
        self.setCentralWidget(self.preview)

        # Timeline dock (bottom)
        self.timeline = TimelineWidget()
        self.timeline_dock = QDockWidget("Timeline", self)
        self.timeline_dock.setObjectName("timelineDock")
        self.timeline_dock.setWidget(self.timeline)
        self.timeline_dock.setFeatures(
            QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable
        )
        self.addDockWidget(Qt.BottomDockWidgetArea, self.timeline_dock)

        # Settings dock (right)
        from ui.settings_panel import SettingsPanel

        self.settings_panel = SettingsPanel()
        self.settings_dock = QDockWidget("Settings", self)
        self.settings_dock.setObjectName("settingsDock")
        self.settings_dock.setWidget(self.settings_panel)
        self.settings_dock.setFeatures(
            QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable
        )
        self.addDockWidget(Qt.RightDockWidgetArea, self.settings_dock)

    def _build_menu(self):
        from PySide6.QtWidgets import QLabel
        from PySide6.QtCore import Qt

        self.menu_bar = MenuBar()
        self.setMenuBar(self.menu_bar)

        # Overlay a centered status label directly on top of the menu bar.
        # WA_TransparentForMouseEvents lets all clicks pass through to the
        # menu items underneath.
        self.status_label = QLabel("Ready", self.menu_bar)
        self.status_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet(
            "color: #A1A1AA; font-size: 9.5pt; border: none; background: transparent;"
        )

        # Keep the overlay sized to the full menu bar on every resize
        orig_resize = self.menu_bar.resizeEvent

        def _menu_bar_resize(event):
            orig_resize(event)
            self.status_label.setGeometry(
                0, 0, self.menu_bar.width(), self.menu_bar.height()
            )

        self.menu_bar.resizeEvent = _menu_bar_resize

    def _connect_signals(self):
        # Preview

        self.preview.openVideoRequested.connect(self.open_video)

        self.preview.videoDropped.connect(self.load_video)

        self.menu_bar.openRequested.connect(self.open_video)

        self.menu_bar.importUrlRequested.connect(self.import_from_url)

        self.menu_bar.exitRequested.connect(self.close)

        self.menu_bar.aboutRequested.connect(self.show_about)
        
        self.menu_bar.themesRequested.connect(self.show_themes)

    def open_video(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Video",
            "",
            ("Video Files " "(*.mp4 *.mov *.avi *.mkv *.webm *.m4v *.mpeg *.mpg)"),
        )

        if file_path:
            self.load_video(file_path)

    def load_video(self, file_path: str):
        self.preview.load_video(file_path)

        self.status_label.setText(f"Loaded: {Path(file_path).name}")

        self.menu_bar.export_action.setEnabled(True)

    def import_from_url(self):
        dialog = ImportUrlDialog(self)
        dialog.videoReady.connect(self.load_video)
        dialog.exec()

    def show_about(self):
        dialogue = AboutDialogue(self)
        dialogue.exec()

    def show_themes(self):
        from ui.theme_dialog import ThemeDialog
        dialogue = ThemeDialog(self)
        dialogue.exec()
