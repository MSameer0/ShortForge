from PySide6.QtCore import Signal
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QMenuBar


class MenuBar(QMenuBar):
    """
    Main application menu bar.

    This class is responsible only for constructing menus and
    emitting signals when actions are triggered.
    """

    openRequested = Signal()
    importUrlRequested = Signal()
    exportRequested = Signal()
    exitRequested = Signal()
    aboutRequested = Signal()
    themesRequested = Signal()

    def __init__(self):
        super().__init__()

        self._build_menus()

    def _build_menus(self):
        self.file_menu = self.addMenu("&File")
        self.view_menu = self.addMenu("&View")
        self.help_menu = self.addMenu("&Help")

        # View
        self.themes_action = QAction("&Themes...", self)
        self.themes_action.setShortcut("Ctrl+T")
        self.themes_action.triggered.connect(self.themesRequested.emit)
        self.view_menu.addAction(self.themes_action)

        # File

        self.open_action = QAction("&Open...", self)
        self.open_action.setShortcut(QKeySequence.StandardKey.Open)
        self.open_action.triggered.connect(self.openRequested.emit)

        self.import_url_action = QAction("Import from &URL...", self)
        self.import_url_action.setShortcut("Ctrl+U")
        self.import_url_action.triggered.connect(self.importUrlRequested.emit)

        self.export_action = QAction("&Export...", self)
        self.export_action.setShortcut("Ctrl+E")
        self.export_action.setEnabled(False)
        self.export_action.triggered.connect(self.exportRequested.emit)

        self.exit_action = QAction("E&xit", self)
        self.exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        self.exit_action.triggered.connect(self.exitRequested.emit)

        self.file_menu.addAction(self.open_action)
        self.file_menu.addAction(self.import_url_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.export_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_action)

        # Help

        self.about_action = QAction("&About ShortForge", self)
        self.about_action.triggered.connect(self.aboutRequested.emit)

        self.help_menu.addAction(self.about_action)
