from PySide6.QtWidgets import * 
from PySide6.QtGui import * 
from PySide6.QtCore import Qt, QTimer
import sys

class Overlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.BypassWindowManagerHint | Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(screen)
        self.showFullScreen()

        self.manager = None
        #self.settings = None
        self.config = None

        self.setTimer()

    # def set_draw_manager(self, manager):
    #     self.manager = manager

    # def set_settings(self, settings):
    #     self.config = settings

    #Timer that reasserts the overlay as the topmost app, keeps it first
    def setTimer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.raise_)
        self.timer.start(1000)

    def paintEvent(self, event):
        if not self.manager or not self.config:
            return

        painter = QPainter(self)
        for drawer, rect in self.manager.get_draw_commands(self.config, self.rect()):
            drawer.draw(painter, rect)
    