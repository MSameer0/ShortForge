from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QTextEdit,
    QInputDialog,
    QMessageBox,
)

from utils.theme_manager import theme_manager


class ThemeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Theme Manager")
        self.resize(700, 600)
        self.setModal(True)

        self._build_ui()
        self._populate_themes()
        self._connect_signals()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        # Top Bar: Theme selection and New Theme button
        top_layout = QHBoxLayout()
        self.theme_combo = QComboBox()
        self.btn_new_theme = QPushButton("New Theme from Current")
        
        top_layout.addWidget(QLabel("Select Theme:"))
        top_layout.addWidget(self.theme_combo, stretch=1)
        top_layout.addWidget(self.btn_new_theme)
        layout.addLayout(top_layout)

        # Editor area
        layout.addWidget(QLabel("Theme Stylesheet (QSS):"))
        self.editor = QTextEdit()
        # Use a monospace font for code
        self.editor.setStyleSheet("font-family: Consolas, monospace; font-size: 10pt;")
        layout.addWidget(self.editor, stretch=1)

        # Bottom Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.btn_cancel = QPushButton("Cancel")
        self.btn_apply = QPushButton("Apply & Save")
        self.btn_apply.setDefault(True)

        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_apply)
        layout.addLayout(btn_layout)

    def _populate_themes(self):
        self.theme_combo.blockSignals(True)
        self.theme_combo.clear()
        
        all_themes = theme_manager.get_all_theme_names()
        self.theme_combo.addItems(all_themes)
        
        idx = self.theme_combo.findText(theme_manager.active_theme_name)
        if idx >= 0:
            self.theme_combo.setCurrentIndex(idx)
            
        self.editor.setPlainText(theme_manager.get_active_style())
        
        # Disable editing if it's a built-in theme
        is_builtin = theme_manager.active_theme_name in theme_manager.built_in
        self.editor.setReadOnly(is_builtin)
        
        self.theme_combo.blockSignals(False)

    def _connect_signals(self):
        self.theme_combo.currentTextChanged.connect(self._on_theme_selected)
        self.btn_new_theme.clicked.connect(self._on_new_theme)
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_apply.clicked.connect(self._on_apply)

    def _on_theme_selected(self, name: str):
        self.editor.setPlainText(theme_manager.get_theme_style(name))
        is_builtin = name in theme_manager.built_in
        self.editor.setReadOnly(is_builtin)

    def _on_new_theme(self):
        name, ok = QInputDialog.getText(
            self, "New Theme", "Enter a name for your new theme profile:"
        )
        if ok and name:
            name = name.strip()
            if not name:
                return
            if name in theme_manager.get_all_theme_names():
                QMessageBox.warning(self, "Error", "A theme with this name already exists.")
                return
                
            # Create new theme with current editor contents
            theme_manager.save_custom_theme(name, self.editor.toPlainText())
            
            # Refresh UI
            self._populate_themes()
            idx = self.theme_combo.findText(name)
            self.theme_combo.setCurrentIndex(idx)

    def _on_apply(self):
        current_name = self.theme_combo.currentText()
        
        # If it's a custom theme, save the editor contents
        if current_name not in theme_manager.built_in:
            theme_manager.save_custom_theme(current_name, self.editor.toPlainText())
            
        # Set as active
        theme_manager.set_active_theme(current_name)
        self.accept()
