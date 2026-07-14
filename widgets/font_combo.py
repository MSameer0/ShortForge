from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtWidgets import QComboBox, QStyledItemDelegate, QStyleOptionViewItem


class FontPreviewDelegate(QStyledItemDelegate):
    """Delegate that renders each font name using the font itself."""

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        font_family = index.data(Qt.DisplayRole)
        # Use the actual font for rendering, with a slightly larger size for readability
        option.font = QFont(font_family, 13)

    def sizeHint(self, option, index):
        # Ensure there is enough vertical space for the custom font
        return QSize(0, 32)


class FontComboBox(QComboBox):
    """
    A drop-down combo box that lists all installed fonts.
    Each item is rendered using the font itself so it acts as a live preview.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEditable(False)
        self.setItemDelegate(FontPreviewDelegate(self))

        # Populate with all installed font families
        families = sorted(set(QFontDatabase.families()))
        self.addItems(families)

        # Default to Arial
        idx = self.findText("Arial")
        if idx >= 0:
            self.setCurrentIndex(idx)

    def currentFontFamily(self) -> str:
        return self.currentText()

    def setCurrentFontFamily(self, family: str):
        idx = self.findText(family)
        if idx >= 0:
            self.setCurrentIndex(idx)
