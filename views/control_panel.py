from PySide6.QtWidgets import QWidget, QComboBox, QCheckBox, QVBoxLayout, QHBoxLayout, QApplication, QPushButton, QSlider, QFrame
from PySide6.QtCore import Qt, QDir
from PySide6.QtGui import QIcon
from utils.paths import get_resource_path
import keyboard
import ctypes
import threading
import sys

class ControlPanel(QWidget):
    def __init__(self):
        super().__init__()

        #self.overlay = overlay

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setWindowTitle("ScreenBuddy Menu")

        self.aspect_ratio_selector = QComboBox()
        self.aspect_ratio_selector.addItems(["None", "9:16", "4:3", "1:1"])

        self.composition_selector = QComboBox()
        self.composition_selector.addItems(["Rule of Thirds", "Horizon Line", "None"])
        
        self.reticle_toggle = QCheckBox("Show Reticle")

        self.crosshair_toggle = QCheckBox("Show Crosshairs")

        self.overlay_toggle = QCheckBox("Overlay Visibility")
        self.overlay_toggle.setChecked(True) #move to model/settings.py, figure out a save state for presets and profiles memory

        self.onion_button = QPushButton("Onion")
        self.onion_button.setIcon(QIcon(get_resource_path("images/CameraIcon.png")))
        self.onion_slider = QSlider(Qt.Orientation.Horizontal)
        self.onion_slider.setMinimum(0)
        self.onion_slider.setMaximum(100)

        self.button_quit = QPushButton("Quit ScreenBuddy")

        layout = QVBoxLayout()
        HboxLayoutDropdown = QHBoxLayout()
        HboxLayoutDropdown.addWidget(self.aspect_ratio_selector)
        HboxLayoutDropdown.addWidget(self.composition_selector)
        layout.addLayout(HboxLayoutDropdown)

        VBoxLayoutCheckboxes = QVBoxLayout()
        VBoxLayoutCheckboxes.addWidget(self.reticle_toggle)
        VBoxLayoutCheckboxes.addWidget(self.crosshair_toggle)
        VBoxLayoutCheckboxes.addWidget(self.overlay_toggle)

        #Added self to qframe so garbage collector doesnt remove it
        self.VBoxFrame = QFrame()
        self.VBoxFrame.setFrameShape(QFrame.Shape.Box)
        self.VBoxFrame.setLineWidth(2)
        VBoxLayoutOnion = QVBoxLayout(self.VBoxFrame)
        VBoxLayoutOnion.addWidget(self.onion_button)
        VBoxLayoutOnion.addWidget(self.onion_slider)

        HBoxMiddleThird = QHBoxLayout()
        HBoxMiddleThird.addLayout(VBoxLayoutCheckboxes)
        HBoxMiddleThird.addWidget(self.VBoxFrame)

        layout.addLayout(HBoxMiddleThird)
        layout.addWidget(self.button_quit)

        self.setLayout(layout)
        self.resize(150, 100)
    
    def closeEvent(self, event):
        QApplication.quit()