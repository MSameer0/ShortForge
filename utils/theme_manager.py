import json
from PySide6.QtCore import QSettings, QObject, Signal
from ui.styles import APP_STYLE as DEFAULT_DARK

def generate_light_theme(dark_qss: str) -> str:
    # Use intermediate placeholders to prevent sequential replacement collisions
    replacements = {
        "#111114": "{bg_main}",       # #F4F4F5
        "#18181B": "{bg_panel}",      # #FFFFFF
        "#27272A": "{border_main}",   # #E4E4E7
        "#1E1E22": "{bg_button}",     # #F4F4F5
        "#3F3F46": "{border_hover}",  # #D4D4D8
        "#E4E4E7": "{text_primary}",  # #18181B
        "#A1A1AA": "{text_secondary}",# #52525B
    }
    
    light_qss = dark_qss
    for k, v in replacements.items():
        light_qss = light_qss.replace(k, v)
        
    final_replacements = {
        "{bg_main}": "#F4F4F5",
        "{bg_panel}": "#FFFFFF",
        "{border_main}": "#E4E4E7",
        "{bg_button}": "#F4F4F5",
        "{border_hover}": "#D4D4D8",
        "{text_primary}": "#18181B",
        "{text_secondary}": "#52525B",
    }
    
    for k, v in final_replacements.items():
        light_qss = light_qss.replace(k, v)
        
    return light_qss

DEFAULT_LIGHT = generate_light_theme(DEFAULT_DARK)

def generate_ice_theme(dark_qss: str) -> str:
    replacements = {
        "#111114": "{bg_main}",       
        "#18181B": "{bg_panel}",      
        "#27272A": "{border_main}",   
        "#1E1E22": "{bg_button}",     
        "#3F3F46": "{border_hover}",  
        "#E4E4E7": "{text_primary}",  
        "#A1A1AA": "{text_secondary}",
        "#8B5CF6": "{accent_primary}",
        "#7C3AED": "{accent_secondary}",
        "#6D28D9": "{accent_pressed}",
    }
    
    ice_qss = dark_qss
    for k, v in replacements.items():
        ice_qss = ice_qss.replace(k, v)
        
    final_replacements = {
        "{bg_main}": "#0F172A",      # Slate-900 (Deep dark blue)
        "{bg_panel}": "#1E293B",     # Slate-800
        "{border_main}": "#334155",  # Slate-700
        "{bg_button}": "#1E293B",    # Slate-800
        "{border_hover}": "#475569", # Slate-600
        "{text_primary}": "#F1F5F9", # Slate-100
        "{text_secondary}": "#94A3B8",# Slate-400
        "{accent_primary}": "#06B6D4",# Cyan-500 (Aqua)
        "{accent_secondary}": "#0891B2",# Cyan-600
        "{accent_pressed}": "#0E7490", # Cyan-700
    }
    
    for k, v in final_replacements.items():
        ice_qss = ice_qss.replace(k, v)
        
    return ice_qss

DEFAULT_ICE = generate_ice_theme(DEFAULT_DARK)

class ThemeManager(QObject):
    themeChanged = Signal(str)  # emits the new stylesheet string

    def __init__(self):
        super().__init__()
        self.settings = QSettings("ShortForge", "ShortForgeApp")
        
        self.built_in = {
            "Dark": DEFAULT_DARK,
            "Light": DEFAULT_LIGHT,
            "Ice": DEFAULT_ICE
        }
        
        self._load_custom_themes()
        
        # Load active theme name, default to Dark
        self.active_theme_name = self.settings.value("active_theme", "Dark")
        if self.active_theme_name not in self.get_all_theme_names():
            self.active_theme_name = "Dark"

    def _load_custom_themes(self):
        # Stored as a JSON string for simplicity
        themes_json = self.settings.value("custom_themes", "{}")
        try:
            self.custom_themes = json.loads(themes_json)
        except Exception:
            self.custom_themes = {}

    def _save_custom_themes(self):
        self.settings.setValue("custom_themes", json.dumps(self.custom_themes))

    def get_all_theme_names(self):
        return list(self.built_in.keys()) + list(self.custom_themes.keys())

    def get_theme_style(self, name: str) -> str:
        if name in self.built_in:
            return self.built_in[name]
        return self.custom_themes.get(name, DEFAULT_DARK)

    def set_active_theme(self, name: str):
        if name in self.get_all_theme_names():
            self.active_theme_name = name
            self.settings.setValue("active_theme", name)
            self.themeChanged.emit(self.get_theme_style(name))

    def save_custom_theme(self, name: str, style: str):
        # Don't overwrite built-ins
        if name in self.built_in:
            return
        self.custom_themes[name] = style
        self._save_custom_themes()

    def get_active_style(self) -> str:
        return self.get_theme_style(self.active_theme_name)

    @property
    def is_light_theme(self) -> bool:
        # Simple heuristic: if the theme is exactly "Light" or has "Light" in the name,
        # or if its background main color string is present
        style = self.get_active_style()
        return "#F4F4F5" in style or "Light" in self.active_theme_name

    @property
    def accent_color(self) -> str:
        style = self.get_active_style()
        # Look for our known accent colors in the style string
        if "#06B6D4" in style:
            return "#06B6D4"
        return "#8B5CF6"

# Global instance
theme_manager = ThemeManager()
