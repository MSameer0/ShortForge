import cv2
import numpy as np
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QImage, QPainter, QColor, QFont, QPen
from PySide6.QtWidgets import QWidget
from PySide6.QtMultimedia import QVideoFrame

from utils.project import active_project


def qimage_to_numpy(image: QImage) -> np.ndarray:
    """
    Convert a QImage (Format_RGB888) to a numpy array.
    Works with both old (sip.voidptr) and new (memoryview) PySide6 APIs.
    """
    w = image.width()
    h = image.height()
    bpl = image.bytesPerLine()

    # .bits() returns memoryview in PySide6 >= 6.7
    ptr = image.bits()
    arr = np.frombuffer(bytes(ptr), dtype=np.uint8)

    # bytesPerLine may include padding, so reshape with stride
    if bpl == w * 3:
        arr = arr.reshape((h, w, 3))
    else:
        arr = arr.reshape((h, bpl))[:, : w * 3].reshape((h, w, 3))

    return arr.copy()


class PreviewRenderer(QWidget):
    """
    Custom widget to render video frames, apply background blur,
    enforce 9:16 aspect ratio, and draw text overlays.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_image = None
        self.current_pos_ms = 0

        # State for dragging
        self.dragging_layer_index = -1
        self.drag_offset_x = 0
        self.drag_offset_y = 0

        # Subscribe to project changes to trigger repaint even when paused
        active_project.settingsChanged.connect(self.update)

    def set_position(self, pos_ms: int):
        self.current_pos_ms = pos_ms
        self.update()

    def set_frame(self, frame: QVideoFrame):
        if not frame.isValid():
            return

        # Convert QVideoFrame to QImage
        image = frame.toImage()
        if image.isNull():
            return

        # Ensure it's in a format we can easily process
        image = image.convertToFormat(QImage.Format_RGB888)
        self.current_image = image
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        # Fill background with black
        painter.fillRect(self.rect(), Qt.black)

        if not self.current_image:
            return

        # Calculate 9:16 aspect ratio rect
        widget_w = self.width()
        widget_h = self.height()

        target_w = widget_w
        target_h = int(widget_w * (16 / 9))

        if target_h > widget_h:
            target_h = widget_h
            target_w = int(widget_h * (9 / 16))

        x_offset = (widget_w - target_w) // 2
        y_offset = (widget_h - target_h) // 2

        preview_rect = QRect(x_offset, y_offset, target_w, target_h)

        # Store canvas width so encoder can scale fonts proportionally
        active_project.preview_canvas_w = target_w

        # 1. Draw Background (blur or black)
        if active_project.blur_background:
            arr = qimage_to_numpy(self.current_image)

            # Scale to fill the 9:16 frame (fit to height)
            img_h, img_w = arr.shape[:2]
            scale = target_h / img_h
            scaled_w = int(img_w * scale)
            bg_arr = cv2.resize(arr, (scaled_w, target_h))

            # Center-crop to target width
            cx = (scaled_w - target_w) // 2
            if cx > 0:
                bg_arr = bg_arr[:, cx : cx + target_w]
            else:
                # Pad horizontally if needed
                pad = (target_w - scaled_w) // 2
                bg_arr = cv2.copyMakeBorder(
                    bg_arr, 0, 0, pad, target_w - scaled_w - pad, cv2.BORDER_REFLECT
                )

            # Apply blur
            ksize = int(active_project.blur_intensity) * 2 + 1
            ksize = max(3, min(ksize, 201))
            bg_arr = cv2.GaussianBlur(bg_arr, (ksize, ksize), 0)

            # Darken slightly
            bg_arr = (bg_arr * 0.6).astype(np.uint8)

            # Convert back to QImage
            h, w = bg_arr.shape[:2]
            bg_image = QImage(bg_arr.data, w, h, w * 3, QImage.Format_RGB888)
            painter.drawImage(preview_rect, bg_image)
        else:
            painter.fillRect(preview_rect, QColor("#000000"))

        # 2. Draw Foreground Video (scaled to fit width)
        img_w = self.current_image.width()
        img_h = self.current_image.height()

        fg_w = target_w
        fg_h = int(img_h * (target_w / img_w))

        if fg_h > target_h:
            fg_h = target_h
            fg_w = int(img_w * (target_h / img_h))

        fg_x = x_offset + (target_w - fg_w) // 2
        fg_y = y_offset + (target_h - fg_h) // 2

        fg_rect = QRect(fg_x, fg_y, fg_w, fg_h)
        painter.drawImage(fg_rect, self.current_image)

        # 3. Draw Text Layers
        for i, layer in enumerate(active_project.text_layers):
            if layer.start_ms <= self.current_pos_ms <= layer.end_ms:
                font = QFont(layer.font_family, layer.font_size, QFont.Bold)
                painter.setFont(font)

                fm = painter.fontMetrics()
                text_width = fm.horizontalAdvance(layer.text)
                text_height = fm.height()

                center_x = x_offset + int(target_w * layer.x_position_ratio)
                center_y = y_offset + int(target_h * layer.y_position_ratio)

                # Top left corner of the text
                text_x = center_x - text_width // 2
                text_y = center_y - text_height // 2

                text_rect = QRect(text_x, text_y, text_width, text_height)

                from PySide6.QtGui import QPainterPath

                path = QPainterPath()

                # addText uses the baseline for the y-coordinate
                baseline_y = text_y + fm.ascent()
                path.addText(text_x, baseline_y, font, layer.text)

                # Draw stroke/outline if width > 0
                if layer.stroke_width > 0:
                    outline_pen = QPen(QColor(layer.stroke_color))
                    outline_pen.setWidth(
                        layer.stroke_width * 2
                    )  # Qt draws pen centered on path
                    outline_pen.setJoinStyle(Qt.RoundJoin)
                    painter.strokePath(path, outline_pen)

                # Fill main text
                painter.fillPath(path, QColor(layer.color))

                # Draw a subtle dashed outline if dragging this layer
                if i == self.dragging_layer_index:
                    pen = QPen(QColor("#8B5CF6"))
                    pen.setStyle(Qt.DashLine)
                    pen.setWidth(2)
                    painter.setPen(pen)
                    painter.drawRect(text_rect.adjusted(-4, -4, 4, 4))

    # Dragging text layers
    def mousePressEvent(self, event):
        if not self.current_image:
            return

        # Calculate target dimensions and offsets to map click correctly
        widget_w = self.width()
        widget_h = self.height()
        target_w = widget_w
        target_h = int(widget_w * (16 / 9))
        if target_h > widget_h:
            target_h = widget_h
            target_w = int(widget_h * (9 / 16))

        x_offset = (widget_w - target_w) // 2
        y_offset = (widget_h - target_h) // 2

        click_x = event.position().x()
        click_y = event.position().y()

        # Check layers in reverse order (top-most first)
        for i in range(len(active_project.text_layers) - 1, -1, -1):
            layer = active_project.text_layers[i]
            if layer.start_ms <= self.current_pos_ms <= layer.end_ms:
                font = QFont(layer.font_family, layer.font_size, QFont.Bold)
                # Need QFontMetrics to get bounding box
                from PySide6.QtGui import QFontMetrics

                fm = QFontMetrics(font)
                text_width = fm.horizontalAdvance(layer.text)
                text_height = fm.height()

                center_x = x_offset + int(target_w * layer.x_position_ratio)
                center_y = y_offset + int(target_h * layer.y_position_ratio)

                text_x = center_x - text_width // 2
                text_y = center_y - text_height // 2

                rect = QRect(text_x, text_y, text_width, text_height)

                if rect.contains(int(click_x), int(click_y)):
                    self.dragging_layer_index = i
                    self.drag_offset_x = click_x - center_x
                    self.drag_offset_y = click_y - center_y
                    self.update()
                    return

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.dragging_layer_index != -1:
            layer = active_project.text_layers[self.dragging_layer_index]

            widget_w = self.width()
            widget_h = self.height()
            target_w = widget_w
            target_h = int(widget_w * (16 / 9))
            if target_h > widget_h:
                target_h = widget_h
                target_w = int(widget_h * (9 / 16))

            x_offset = (widget_w - target_w) // 2
            y_offset = (widget_h - target_h) // 2

            click_x = event.position().x()
            click_y = event.position().y()

            new_center_x = click_x - self.drag_offset_x
            new_center_y = click_y - self.drag_offset_y

            layer.x_position_ratio = (new_center_x - x_offset) / target_w
            layer.y_position_ratio = (new_center_y - y_offset) / target_h

            self.update()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.dragging_layer_index != -1:
            self.dragging_layer_index = -1
            active_project.settingsChanged.emit()  # Save state
            self.update()
        else:
            super().mouseReleaseEvent(event)
