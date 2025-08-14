from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import QRect

class CrosshairDrawer:
    def __init__(self, color: QColor):
        self.color = color

    def draw(self, painter: QPainter, rect: QRect):
        painter.save()
        pen = painter.pen()
        pen.setColor(self.color)
        pen.setWidth(2)
        painter.setPen(pen)

        center_x = rect.center().x()
        center_y = rect.center().y()

        # Simple crosshair lines (20px long)
        length = 20
        painter.drawLine(center_x - length, center_y, center_x + length, center_y)
        painter.drawLine(center_x, center_y - length, center_x, center_y + length)

        painter.restore()