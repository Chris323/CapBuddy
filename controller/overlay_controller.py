import keyboard
import threading
from PySide6.QtWidgets import * 
from PySide6.QtGui import * 
from PySide6.QtCore import Qt

class OverlayConfig:
    def __init__(self):
        self.aspect_ratio = "None"
        self.composition = "None"
        self.show_crosshair = False
        self.show_reticle = False

class OverlayController:
    def __init__(self, overlay, control_panel, drawer_manager, settings=None):
        self.overlay = overlay
        self.control_panel = control_panel
        self.drawer_manager = drawer_manager
        #self.settings = settings

        self.config = None

        self.setup_signals()
        self._create_hotkey_listener()

    def setup_signals(self):
        self.control_panel.aspect_ratio_selector.currentTextChanged.connect(self.aspect_ratio_cbox_selector)
        self.control_panel.composition_selector.currentTextChanged.connect(self.composition_cbox_selector)
        self.control_panel.reticle_toggle.toggled.connect(self.show_reticle_toggle)
        self.control_panel.crosshair_toggle.toggled.connect(self.show_crosshairs_toggle)
        self.control_panel.overlay_toggle.toggled.connect(self.show_overlay_toggle)
        self.control_panel.button_quit.clicked.connect(self.quit_app)

    def aspect_ratio_cbox_selector(self, text):
        self.config.aspect_ratio = text
        self.overlay.update()

    def composition_cbox_selector(self, text):
        self.config.composition = text
        self.overlay.update()

    def show_reticle_toggle(self, checked):
        self.config.show_reticle = checked
        self.overlay.update()

    def show_crosshairs_toggle(self, checked):
        self.config.show_crosshair = checked
        self.overlay.update()
    
    def show_overlay_toggle(self, checked=None):
        if checked is None:
        # Hotkey was pressed → manually toggle the checkbox
            current = self.control_panel.overlay_toggle.isChecked()
            self.control_panel.overlay_toggle.setChecked(not current)
            return
        #toggled(bool) is emitted, once again entering this function through the signal, skipping the if statement

    # If 'checked' toggled and is a bool, update the overlay
        self.overlay.setVisible(checked)


    def cycle_colors(self):
        self.drawer_manager.cycle_color()
        # Trigger repaint on overlay so new colors show
        self.overlay.update()

    #Global hotkey for toggling visibility
    def _create_hotkey_listener(self):
        def listener():
            keyboard.add_hotkey("F10", self.show_overlay_toggle)
            keyboard.add_hotkey("F9", self.cycle_colors)

            keyboard.wait()  # Keeps the thread alive

        thread = threading.Thread(target=listener, daemon=True)
        thread.start()


    def quit_app(self):
        QApplication.quit()