import keyboard
import threading
from PySide6.QtWidgets import * 
from PySide6.QtGui import * 
from PySide6.QtCore import Qt, QTimer

class OverlayConfig:
    def __init__(self):
        self.aspect_ratio = "None"
        self.composition = "Rule of Thirds"
        self.show_crosshair = False
        self.show_reticle = False

        self.screenshot = False
        self.opacity_value = 0

class OverlayController:
    def __init__(self, overlay, control_panel, drawer_manager, settings=None):
        self.overlay = overlay
        self.control_panel = control_panel
        self.drawer_manager = drawer_manager

        #self.settings = settings
        ##Config is temp, until settings get implemented
        self.config = None
        
        #Timer
        self.cooldown_timer = QTimer()

        self.setup_signals()
        self._create_hotkey_listener()

    #3#The config is updated here, which in turn updates the overlay_draw_manager and self.config here. The update() ensures this, these signal are connected through the main.py
    def setup_signals(self):
        self.control_panel.aspect_ratio_selector.currentTextChanged.connect(self.aspect_ratio_cbox_selector)
        self.control_panel.composition_selector.currentTextChanged.connect(self.composition_cbox_selector)
        self.control_panel.reticle_toggle.toggled.connect(self.show_reticle_toggle)
        self.control_panel.crosshair_toggle.toggled.connect(self.show_crosshairs_toggle)
        self.control_panel.overlay_toggle.toggled.connect(self.show_overlay_toggle)
        self.control_panel.button_quit.clicked.connect(self.quit_app)
        self.control_panel.onion_button.clicked.connect(self.onion_screenshot)
        self.control_panel.onion_slider.valueChanged.connect(self.opacity_slider)

    #Slots
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
        ##If checked (defaulted to none) is not clicked on but this slot is called through a hotkey, "If" triggers. Checked is the status of the box
        ##clicking the checkbox swaps between true and false and sends its current status. 
        if checked is None:
        # Hotkey was pressed -> manually toggle the checkbox
            current = self.control_panel.overlay_toggle.isChecked()
            self.control_panel.overlay_toggle.setChecked(not current)
            return
        #toggled(bool) is emitted, once again entering this function through the signal, skipping the if statement

    # If 'checked' toggled by clicking and is a bool, update the overlay
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

    def onion_screenshot(self):
        #print("Onion Pressed")
        self.config.screenshot = True
        self.drawer_manager.screenshot.save_screenshot()
        self.control_panel.onion_slider.setValue(0)
        #The next lines disable the button for 1 second, update the overlay and reenable the button)
        self.control_panel.onion_button.setEnabled(False)
        self.overlay.update()
        self.cooldown_timer.singleShot(1000, lambda: self.control_panel.onion_button.setEnabled(True))


    def opacity_slider(self):
        #print(f"Slider value: {float(self.control_panel.onion_slider.value())} Data type:{type(float(self.control_panel.onion_slider.value()))}")
        current_opacity_value = float(self.control_panel.onion_slider.value()) * 0.01
        #print(opacity_value)
        self.drawer_manager.screenshot.setOpacity(current_opacity_value)
        self.config.opacity_value = current_opacity_value
        self.overlay.update()

    def quit_app(self):
        QApplication.quit()