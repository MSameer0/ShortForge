from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)

from utils.app_info import (
    APP_NAME,
    VERSION,
    AUTHOR,
    COPYRIGHT,
    DESCRIPTION,
    REPOSITORY,
)


class AboutDialogue(QDialog):
    """
    About ShortForge.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle(f"About {APP_NAME}")
        self.setModal(True)
        self.setFixedWidth(480)

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        title = QLabel(APP_NAME)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
        """)

        layout.addWidget(title)

        version = QLabel(f"Version {VERSION}")
        version.setAlignment(Qt.AlignCenter)

        layout.addWidget(version)

        description = QLabel(DESCRIPTION)
        description.setAlignment(Qt.AlignCenter)
        description.setWordWrap(True)

        layout.addWidget(description)

        author = QLabel(AUTHOR)
        author.setAlignment(Qt.AlignCenter)

        layout.addWidget(author)

        copyright_label = QLabel(COPYRIGHT)
        copyright_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(copyright_label)

        feature_req = QLabel(
            '<a href="https://github.com/YourUsername/ShortForge/issues/new" style="color: #8B5CF6; text-decoration: none;">Want to request a feature? Click here.</a>'
        )
        feature_req.setAlignment(Qt.AlignCenter)
        feature_req.setOpenExternalLinks(True)
        layout.addWidget(feature_req)

        contribute_link = QLabel(
            '<a href="https://github.com/YourUsername/ShortForge/blob/main/CONTRIBUTING.md" style="color: #8B5CF6; text-decoration: none;">Want to contribute to this project? Click here.</a>'
        )
        contribute_link.setAlignment(Qt.AlignCenter)
        contribute_link.setOpenExternalLinks(True)
        layout.addWidget(contribute_link)

        layout.addStretch()

        buttons = QHBoxLayout()

        github = QPushButton("GitHub")
        close = QPushButton("Close")

        github.clicked.connect(self.open_repository)
        close.clicked.connect(self.accept)

        buttons.addWidget(github)
        buttons.addStretch()
        buttons.addWidget(close)

        layout.addLayout(buttons)

    def open_repository(self):
        QDesktopServices.openUrl(QUrl(REPOSITORY))
