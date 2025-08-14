from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import QRect

class DotReticleDrawer:
    def __init__(self, color: QColor):
        self.color = color

    def draw(self, painter: QPainter, rect: QRect):
        painter.save()
        pen = painter.pen()
        pen.setColor(self.color)
        pen.setWidth(4)
        painter.setPen(pen)

        center = rect.center()
        painter.drawPoint(center)

        painter.restore()