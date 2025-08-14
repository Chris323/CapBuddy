from PySide6 import QtWidgets
from views.overlay import Overlay
from views.control_panel import ControlPanel
from model.settings import Settings
from controller.overlay_controller import OverlayController
from views.overlay_drawers.overlay_draw_manager import OverlayDrawerManager
from controller.overlay_controller import OverlayConfig
import sys

# def main():
#     app = QtWidgets.QApplication(sys.argv)

#     overlay = Overlay()
#     control_panel = ControlPanel()  # Your control widget, temporarily using overlay in its constructor
#     control_panel.move(100, 100)
#     settings = Settings()
#     controller = OverlayController(overlay, control_panel, settings) #need to move signals and slots into this class
    
#     overlay.show()
#     control_panel.show()

#     sys.exit(app.exec())

def main():
    app = QtWidgets.QApplication(sys.argv)

    overlay = Overlay()
    control_panel = ControlPanel()
    #settings = Settings()

    drawer_manager = OverlayDrawerManager()
    config = OverlayConfig()
    controller = OverlayController(overlay, control_panel, drawer_manager)

    overlay.manager = drawer_manager  # So overlay.paintEvent can access it
    overlay.config = config
    controller.config = config
    overlay.show()
    control_panel.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
