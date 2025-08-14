from PySide6.QtWidgets import * 
from PySide6.QtGui import * 
from PySide6.QtCore import Qt
import sys

class Overlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.BypassWindowManagerHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(screen)
        self.showFullScreen()

        self.manager = None
        #self.settings = None
        self.config = None

    # def set_draw_manager(self, manager):
    #     self.manager = manager

    # def set_settings(self, settings):
    #     self.config = settings

    def paintEvent(self, event):
        if not self.manager or not self.config:
            return

        painter = QPainter(self)
        for drawer, rect in self.manager.get_draw_commands(self.config, self.rect()):
            drawer.draw(painter, rect)