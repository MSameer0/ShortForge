from PySide6.QtCore import Qt, Signal, QRect
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QPixmap
from PySide6.QtWidgets import QWidget
from utils.theme_manager import theme_manager


class RangeSlider(QWidget):
    rangeChanged = Signal(int, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(100, 50)
        self.setMouseTracking(True)

        self._minimum = 0
        self._maximum = 100
        self._low = 0
        self._high = 100

        self._handle_radius = 8
        self._active_handle = None  # 'low' or 'high'
        self._margin = self._handle_radius + 2

        # Thumbnail strip
        self._thumbnails: list[QPixmap] = []
        
        theme_manager.themeChanged.connect(self.update)

    # ---- value accessors ----

    def setMinimum(self, val):
        self._minimum = val
        self.update()

    def setMaximum(self, val):
        self._maximum = val
        self.update()

    def setLow(self, val):
        self._low = max(self._minimum, min(val, self._high))
        self.update()

    def setHigh(self, val):
        self._high = min(self._maximum, max(val, self._low))
        self.update()

    def setRange(self, min_val, max_val):
        self._minimum = min_val
        self._maximum = max_val
        self.update()

    def low(self):
        return self._low

    def high(self):
        return self._high

    # ---- thumbnails ----

    def set_thumbnails(self, pixmaps: list):
        self._thumbnails = pixmaps
        self.update()

    def thumbnail_strip_height(self) -> int:
        """Height of the thumbnail track area."""
        return self.height() - 4  # small padding

    # ---- coordinate helpers ----

    def _val_to_x(self, val):
        if self._maximum <= self._minimum:
            return self._margin
        ratio = (val - self._minimum) / (self._maximum - self._minimum)
        available_width = self.width() - 2 * self._margin
        return int(self._margin + ratio * available_width)

    def _x_to_val(self, x):
        available_width = self.width() - 2 * self._margin
        if available_width <= 0:
            return self._minimum
        x = max(self._margin, min(x, self.width() - self._margin))
        ratio = (x - self._margin) / available_width
        return int(self._minimum + ratio * (self._maximum - self._minimum))

    # ---- painting ----

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        track_left = self._margin
        track_width = self.width() - 2 * self._margin
        track_top = 2
        track_height = self.height() - 4

        track_rect = QRect(track_left, track_top, track_width, track_height)

        # 1. Draw thumbnail strip or fallback track
        if self._thumbnails:
            # Clip to rounded rect
            painter.save()
            painter.setClipRect(track_rect)

            # Tile thumbnails across the full track width
            n = len(self._thumbnails)
            tile_w = track_width / n if n > 0 else track_width
            for i, pix in enumerate(self._thumbnails):
                dest_x = track_left + int(i * tile_w)
                dest_w = int(tile_w) + 1  # +1 to avoid gaps
                dest_rect = QRect(dest_x, track_top, dest_w, track_height)
                painter.drawPixmap(dest_rect, pix)

            # Dim the unselected regions
            dim_alpha = 100 if theme_manager.is_light_theme else 160
            dim = QColor(255, 255, 255, dim_alpha) if theme_manager.is_light_theme else QColor(0, 0, 0, dim_alpha)
            low_x = self._val_to_x(self._low)
            high_x = self._val_to_x(self._high)

            # Left dim
            if low_x > track_left:
                painter.fillRect(
                    QRect(track_left, track_top, low_x - track_left, track_height), dim
                )
            # Right dim
            if high_x < track_left + track_width:
                painter.fillRect(
                    QRect(
                        high_x,
                        track_top,
                        track_left + track_width - high_x,
                        track_height,
                    ),
                    dim,
                )

            painter.restore()

            # Border around the selected region
            painter.setPen(QPen(QColor(theme_manager.accent_color), 2))
            painter.setBrush(Qt.NoBrush)
            sel_rect = QRect(low_x, track_top, high_x - low_x, track_height)
            painter.drawRoundedRect(sel_rect, 4, 4)
        else:
            # Fallback: solid dark track
            painter.setPen(Qt.NoPen)
            track_color = QColor("#E4E4E7") if theme_manager.is_light_theme else QColor("#27272A")
            painter.setBrush(QBrush(track_color))
            painter.drawRoundedRect(track_rect, 4, 4)

            # Selected range highlight
            low_x = self._val_to_x(self._low)
            high_x = self._val_to_x(self._high)
            selected_rect = QRect(
                low_x, track_top + track_height // 2 - 2, high_x - low_x, 4
            )
            painter.setBrush(QBrush(QColor(theme_manager.accent_color)))
            painter.drawRoundedRect(selected_rect, 2, 2)

        # 2. Draw handles
        low_x = self._val_to_x(self._low)
        high_x = self._val_to_x(self._high)
        y_center = self.height() // 2
        r = self._handle_radius

        for hx in (low_x, high_x):
            # Shadow
            if not theme_manager.is_light_theme:
                painter.setPen(Qt.NoPen)
                painter.setBrush(QBrush(QColor(0, 0, 0, 80)))
                painter.drawEllipse(hx - r, y_center - r + 1, r * 2, r * 2)
            # Handle body
            handle_color = QColor("#FFFFFF") if theme_manager.is_light_theme else QColor("#18181B")
            border_color = QColor("#18181B") if theme_manager.is_light_theme else QColor("#E4E4E7")
            painter.setPen(QPen(border_color, 2))
            painter.setBrush(QBrush(handle_color))
            painter.drawEllipse(hx - r, y_center - r, r * 2, r * 2)

    # ---- mouse interaction ----

    def mousePressEvent(self, event):
        x = event.position().x()
        low_x = self._val_to_x(self._low)
        high_x = self._val_to_x(self._high)

        dist_low = abs(x - low_x)
        dist_high = abs(x - high_x)

        if dist_low < dist_high and dist_low < self._handle_radius * 2:
            self._active_handle = "low"
        elif dist_high < self._handle_radius * 2:
            self._active_handle = "high"
        else:
            self._active_handle = None

    def mouseMoveEvent(self, event):
        if not self._active_handle:
            return

        x = event.position().x()
        val = self._x_to_val(x)

        if self._active_handle == "low":
            self.setLow(val)
        else:
            self.setHigh(val)

        self.rangeChanged.emit(self._low, self._high)

    def mouseReleaseEvent(self, event):
        self._active_handle = None
