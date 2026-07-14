import sys

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow
from utils.theme_manager import theme_manager

def main():
    app = QApplication(sys.argv)

    app.setStyleSheet(theme_manager.get_active_style())
    theme_manager.themeChanged.connect(app.setStyleSheet)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
