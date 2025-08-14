from PySide6.QtCore import QRect
from PySide6.QtGui import QPainter, QColor

class BaseCompositionDrawer:
    def __init__(self, color: QColor):
        self.color = color
    def draw (self, painter: QPainter, rect: QRect):
        raise NotImplementedError("Must be implemented by child class")

class RuleofThirdsDrawer(BaseCompositionDrawer):
    def draw(self, painter: QPainter, rect: QRect):
        painter.save()
        pen = painter.pen()
        pen.setColor(self.color)
        pen.setWidth(2)
        painter.setPen(pen)

        x1 = rect.x() + rect.width() / 3
        x2 = rect.x() + 2 * rect.width() / 3
        y1 = rect.y() + rect.height() / 3
        y2 = rect.y() + 2 * rect.height() / 3

        painter.drawLine(int(x1), int(rect.y()), int(x1), int(rect.y() + rect.height()))
        painter.drawLine(int(x2), int(rect.y()), int(x2), int(rect.y() + rect.height()))
        painter.drawLine(int(rect.x()), int(y1), int(rect.x() + rect.width()), int(y1))
        painter.drawLine(int(rect.x()), int(y2), int(rect.x() + rect.width()), int(y2))
        painter.restore()

class HorizonLineDrawer(BaseCompositionDrawer):
    def draw(self, painter: QPainter, rect: QRect):
        painter.save()
        pen = painter.pen()
        pen.setColor(self.color)
        pen.setWidth(2)
        painter.setPen(pen)

        # Horizon line ~ 1/3 from bottom (artist standard)
        y = rect.y() + rect.height() * 2 / 3
        painter.drawLine(rect.x(), int(y), rect.x() + rect.width(), int(y))

        painter.restore()