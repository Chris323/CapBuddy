from PySide6.QtWidgets import QWidget, QComboBox, QCheckBox, QVBoxLayout, QHBoxLayout, QApplication, QPushButton
from PySide6.QtCore import Qt
import keyboard
import ctypes
import threading
import sys

class ControlPanel(QWidget):
    def __init__(self):
        super().__init__()

        #self.overlay = overlay

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setWindowTitle("CapBuddy Menu")

        self.aspect_ratio_selector = QComboBox()
        self.aspect_ratio_selector.addItems(["None", "9:16", "4:3", "1:1"])

        self.composition_selector = QComboBox()
        self.composition_selector.addItems(["None", "Rule of Thirds", "Horizon Line"])
        
        self.reticle_toggle = QCheckBox("Show Reticle")

        self.crosshair_toggle = QCheckBox("Show Crosshairs")

        self.overlay_toggle = QCheckBox("Overlay Visible")
        self.overlay_toggle.setChecked(True) #move to model/settings.py, figure out a save state for presets and profiles memory

        self.button_quit = QPushButton("Quit CapBuddy")

        layout = QVBoxLayout()
        HboxLayout = QHBoxLayout()
        HboxLayout.addWidget(self.aspect_ratio_selector)
        HboxLayout.addWidget(self.composition_selector)
        layout.addLayout(HboxLayout)
        layout.addWidget(self.reticle_toggle)
        layout.addWidget(self.crosshair_toggle)
        layout.addWidget(self.overlay_toggle)
        layout.addWidget(self.button_quit)

        self.setLayout(layout)
        self.resize(150, 100)
