from PySide6 import QtWidgets
from views.overlay import Overlay
from views.control_panel import ControlPanel
from model.settings import Settings
from controller.overlay_controller import OverlayController
from views.overlay_drawers.overlay_draw_manager import OverlayDrawerManager
from controller.overlay_controller import OverlayConfig
import sys

import ctypes
from controller.hotkeys import GlobalHotKeyFilter, user32, F9_KEY, HOTKEY_ID

def main():
    app = QtWidgets.QApplication(sys.argv)

    overlay = Overlay()
    control_panel = ControlPanel()
    #settings = Settings()
    drawer_manager = OverlayDrawerManager()
    config = OverlayConfig() #Default configuration

    controller = OverlayController(overlay, control_panel, drawer_manager)

    overlay.manager = drawer_manager  # So overlay.paintEvent can access it
    overlay.config = config 
    controller.config = config

    hotkey_filter = GlobalHotKeyFilter(controller.cycle_colors)
    app.installNativeEventFilter(hotkey_filter)
    if not user32.RegisterHotKey(None, HOTKEY_ID, 0, F9_KEY):
        raise RuntimeError("Failed to register F9")
    app.aboutToQuit.connect(lambda: user32.UnregisterHotKey(None, HOTKEY_ID))

    overlay.show()
    control_panel.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
