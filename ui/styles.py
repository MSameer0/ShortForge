APP_STYLE = """
QWidget {
    background-color: #111114;
    color: #E4E4E7;
    font-family: "Segoe UI";
    font-size: 10.5pt;
}

QMainWindow {
    background-color: #111114;
}

QFrame {
    background-color: #18181B;
    border: 1px solid #27272A;
    border-radius: 10px;
}

QLabel {
    color: #E4E4E7;
    background: transparent;
    border: none;
}

QPushButton {
    background-color: #1E1E22;
    border: 1px solid #27272A;
    border-radius: 8px;
    padding: 8px 16px;
    color: #E4E4E7;
}

QPushButton:hover {
    background-color: #27272A;
    border-color: #3F3F46;
}

QPushButton:pressed {
    background-color: #8B5CF6;
    border-color: #8B5CF6;
    color: #FFFFFF;
}

QComboBox {
    background-color: #1E1E22;
    border: 1px solid #27272A;
    border-radius: 8px;
    padding: 6px 10px;
    color: #E4E4E7;
}

QComboBox:hover {
    border-color: #3F3F46;
}

QComboBox::drop-down {
    border: none;
    width: 24px;
}

QComboBox QAbstractItemView {
    background-color: #18181B;
    border: 1px solid #27272A;
    border-radius: 6px;
    selection-background-color: #8B5CF6;
    selection-color: #FFFFFF;
    outline: none;
}

QCheckBox {
    spacing: 8px;
    color: #E4E4E7;
    background: transparent;
    border: none;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 1px solid #3F3F46;
    background-color: #1E1E22;
}

QCheckBox::indicator:hover {
    border-color: #8B5CF6;
}

QCheckBox::indicator:checked {
    background-color: #8B5CF6;
    border-color: #8B5CF6;
    image: none;
}

QSlider::groove:horizontal {
    background: #27272A;
    height: 5px;
    border-radius: 2px;
}

QSlider::handle:horizontal {
    background: #8B5CF6;
    width: 16px;
    height: 16px;
    margin: -6px 0;
    border-radius: 8px;
}

QSlider::handle:horizontal:hover {
    background: #7C3AED;
}

QSlider::sub-page:horizontal {
    background: #8B5CF6;
    border-radius: 2px;
}

QProgressBar {
    border: 1px solid #27272A;
    border-radius: 6px;
    background: #1E1E22;
    text-align: center;
    color: #A1A1AA;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #8B5CF6, stop:1 #7C3AED);
    border-radius: 5px;
}

QMenuBar {
    background-color: #18181B;
    border-bottom: 1px solid #27272A;
}

QMenuBar::item {
    padding: 6px 12px;
    background: transparent;
}

QMenuBar::item:selected {
    background-color: #27272A;
    border-radius: 6px;
}

QMenu {
    background-color: #18181B;
    border: 1px solid #27272A;
    border-radius: 8px;
    padding: 4px;
}

QMenu::item {
    padding: 6px 24px;
    border-radius: 4px;
}

QMenu::item:selected {
    background-color: #8B5CF6;
    color: #FFFFFF;
}

QMenu::separator {
    height: 1px;
    background: #27272A;
    margin: 4px 8px;
}

QStatusBar {
    background-color: #18181B;
    border-top: 1px solid #27272A;
    color: #A1A1AA;
}

QScrollArea {
    background: transparent;
    border: none;
}

QScrollBar:vertical {
    background: transparent;
    width: 6px;
    margin: 0;
    border: none;
}

QScrollBar::handle:vertical {
    background: #3F3F46;
    border-radius: 3px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background: #52525B;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical,
QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: transparent;
    height: 0;
    border: none;
}

QScrollBar:horizontal {
    background: transparent;
    height: 6px;
    margin: 0;
    border: none;
}

QScrollBar::handle:horizontal {
    background: #3F3F46;
    border-radius: 3px;
    min-width: 30px;
}

QScrollBar::handle:horizontal:hover {
    background: #52525B;
}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal,
QScrollBar::add-page:horizontal,
QScrollBar::sub-page:horizontal {
    background: transparent;
    width: 0;
    border: none;
}

#previewFrame {
    background-color: #18181B;
    border: 1px solid #27272A;
    border-radius: 12px;
}

#previewFrame[dragging="true"] {
    border: 2px solid #8B5CF6;
    background-color: #1a1525;
}

#settingsPanel {
    background-color: #18181B;
    border: 1px solid #27272A;
    border-radius: 10px;
}

#settingsDivider {
    background-color: #27272A;
    border: none;
}

#textLayerCard {
    background-color: #1E1E22;
    border: 1px solid #27272A;
    border-radius: 8px;
}

#timelineFrame {
    background-color: #18181B;
    border: 1px solid #27272A;
    border-radius: 10px;
}

#exportButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #8B5CF6, stop:1 #7C3AED);
    border: none;
    border-radius: 8px;
    padding: 10px 16px;
    color: #FFFFFF;
    font-weight: bold;
    font-size: 11pt;
}

#exportButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #7C3AED, stop:1 #6D28D9);
}

#exportButton:pressed {
    background: #6D28D9;
}

QDialog, QInputDialog {
    background-color: #18181B;
    border: 1px solid #27272A;
    border-radius: 10px;
}

QDialog QLabel, QInputDialog QLabel {
    color: #E4E4E7;
    background: transparent;
    border: none;
}

QDialog QLineEdit, QInputDialog QLineEdit {
    background-color: #1E1E22;
    border: 1px solid #27272A;
    border-radius: 6px;
    padding: 6px 10px;
    color: #E4E4E7;
    selection-background-color: #8B5CF6;
}

QDialog QLineEdit:focus, QInputDialog QLineEdit:focus {
    border-color: #8B5CF6;
}

QDialog QPushButton, QInputDialog QPushButton {
    background-color: #1E1E22;
    border: 1px solid #27272A;
    border-radius: 6px;
    padding: 6px 18px;
    color: #E4E4E7;
    min-width: 70px;
}

QDialog QPushButton:hover, QInputDialog QPushButton:hover {
    background-color: #27272A;
    border-color: #3F3F46;
}

QDialog QPushButton:default, QInputDialog QPushButton:default {
    background-color: #8B5CF6;
    border-color: #8B5CF6;
    color: #FFFFFF;
}

QDialog QPushButton:default:hover, QInputDialog QPushButton:default:hover {
    background-color: #7C3AED;
}

QMessageBox {
    background-color: #18181B;
}

QMessageBox QLabel {
    color: #E4E4E7;
    background: transparent;
    border: none;
}

QToolTip {
    background-color: #18181B;
    border: 1px solid #27272A;
    border-radius: 4px;
    padding: 4px 8px;
    color: #E4E4E7;
}

QDockWidget {
    background-color: #111114;
    color: #A1A1AA;
    font-size: 9.5pt;
    titlebar-close-icon: none;
}

QDockWidget::title {
    background-color: #18181B;
    border: 1px solid #27272A;
    border-bottom: none;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    padding: 6px 12px;
    text-align: left;
    color: #A1A1AA;
}

QDockWidget::float-button {
    background: transparent;
    border: none;
    padding: 2px;
}

QDockWidget::float-button:hover {
    background-color: #27272A;
    border-radius: 4px;
}

QMainWindow::separator {
    background-color: #27272A;
    width: 3px;
    height: 3px;
}

QMainWindow::separator:hover {
    background-color: #8B5CF6;
}
"""
