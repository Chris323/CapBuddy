from PySide6 import QtWidgets
from views.overlay import Overlay
from views.control_panel import ControlPanel
from model.settings import Settings
from controller.overlay_controller import OverlayController
from views.overlay_drawers.overlay_draw_manager import OverlayDrawerManager
from controller.overlay_controller import OverlayConfig
import sys

import ctypes
from controller.hotkeys import GlobalHotKeyFilter, user32, VK_F9, VK_F10, HOTKEY_F9_ID, HOTKEY_F10_ID

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

    #Hot key instantiation, adding it to QT loop, error checking, killing process
    hotkey_filter = GlobalHotKeyFilter({HOTKEY_F9_ID: controller.cycle_colors, HOTKEY_F10_ID: controller.show_overlay_toggle})
    app.installNativeEventFilter(hotkey_filter)

    if not user32.RegisterHotKey(None, HOTKEY_F9_ID, 0, VK_F9):
        raise RuntimeError("Failed to register Hotkey F9")
    if not user32.RegisterHotKey(None, HOTKEY_F10_ID, 0, VK_F10):
        raise RuntimeError("Failed to register Hotkey F10")
    app.aboutToQuit.connect(lambda: user32.UnregisterHotKey(None, HOTKEY_F9_ID))
    app.aboutToQuit.connect(lambda: user32.UnregisterHotKey(None, HOTKEY_F10_ID))

    overlay.show()
    control_panel.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
