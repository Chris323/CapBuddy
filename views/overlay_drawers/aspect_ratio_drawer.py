from PySide6.QtCore import QRect
from PySide6.QtGui import QPainter, QColor


class AspectRatioDrawer:
    def __init__(self, color, aspect_width: int, aspect_height: int):
        self.color = color
        self.aspect_width = aspect_width
        self.aspect_height = aspect_height

    def draw(self, painter: QPainter, rect: QRect):
        painter.save()

        # Compute centered rectangle with target aspect ratio
        screen_w, screen_h = rect.width(), rect.height()
        target_w = screen_w
        target_h = target_w * self.aspect_height / self.aspect_width

        if target_h > screen_h:
            target_h = screen_h
            target_w = target_h * self.aspect_width / self.aspect_height

        x = rect.x() + (screen_w - target_w) / 2
        y = rect.y() + (screen_h - target_h) / 2
        aspect_rect = QRect(int(x), int(y), int(target_w), int(target_h))

        # Draw the rectangle
        pen = painter.pen()
        pen.setColor(self.color)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawRect(aspect_rect)

        painter.restore()