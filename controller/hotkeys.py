import ctypes
from ctypes import wintypes
from PySide6.QtCore import QAbstractNativeEventFilter
from PySide6 import QtCore

user32 = ctypes.windll.user32
WM_HOTKEY = 0x0312
F9_KEY = 0x78
HOTKEY_ID = 1

class GlobalHotKeyFilter(QAbstractNativeEventFilter):
    def __init__(self, callback):
        super().__init__()
        self._callback = callback

    def nativeEventFilter(self, eventType, message):
        try:
            if isinstance(eventType, QtCore.QByteArray):
                eventType = bytes(eventType)

            if eventType not in (b"windows_generic_MSG", "windows_generic_MSG"):
                return False, 0

            try:
                addr = int(message)
            except Exception:
                addr = message.address

            msg = wintypes.MSG.from_address(addr)

            if msg.message == WM_HOTKEY and msg.wParam == HOTKEY_ID:
                self._callback()
                return True, 0

            return False, 0

        except Exception as e:
            print("Hotkey filter error:", e)
            return False, 0
