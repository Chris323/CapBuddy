import sys
from PySide6.QtCore import (QDir, QPoint, QRect, QStandardPaths, Qt, QTime, QDateTime)
from PySide6.QtGui import QImageWriter, QImageReader, QPainter, QColor
from PySide6.QtWidgets import QFileDialog, QSizePolicy, QDialog, QMessageBox, QWidget
from utils.paths import get_writable_path
import shutil, os, re, sys

class Screenshot(QWidget):
    def __init__(self):
        super().__init__()
        self.use_counter = 0
        self.original_pixmap = None
        # #Work in Progress
        self.opacity_value = 0

    #Drives this class
    def save_screenshot(self):
        fmt = "png"  # In order to avoid shadowing built-in format
        #Used for standard pictures path on users os profile
        doc_path = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
        initial_path = os.path.join(doc_path, "Screenbuddy", "screenshots")
        #initial_path = get_writable_path("images/screenshots")
        os.makedirs(initial_path, exist_ok=True)
        #activates when directory has has more than 6 or more items stored.
        if len(os.listdir(initial_path)) > 5:
            self.delete_oldest_content(initial_path)
        #Add current day and time to avoid file naming duplication
        time_day = QDateTime()
        current_DT = time_day.currentDateTime()
        current_DT_ISO = current_DT.toString(Qt.DateFormat.ISODate)
        current_DT_ISO = current_DT_ISO.replace(':', '_')   
        initial_path += f"/untitled{current_DT_ISO}.{fmt}"

        self.shoot_screen()

        ##To use save via file dialog box
        # fileDialog = QFileDialog(self, "Save As", initial_path)
        # fileDialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        # fileDialog.setFileMode(QFileDialog.FileMode.AnyFile)
        # #fileDialog.setDirectory(initial_path)
        # mime_types = []
        # #Sets pre-selects for QFileDialog Box
        # for bf in QImageWriter.supportedMimeTypes():
        #     mime_types.append(bf.data().decode("utf8"))
        # fileDialog.setMimeTypeFilters(mime_types)
        # fileDialog.selectMimeTypeFilter("image/" + fmt)
        # fileDialog.setDefaultSuffix(fmt)
        # if fileDialog.exec() != QDialog.DialogCode.Accepted:
        #     return
        ##Attempts to save the file to file path
        #file_name = fileDialog.selectedFiles()[0]


        #print(os.getcwd())
        #print(f"Current path images saved at: {initial_path}")
        if not self.original_pixmap.save(initial_path):
            path = QDir.toNativeSeparators(initial_path)
            QMessageBox.warning(
                self,
                "Save Error",
                f"The image could not be saved to {path}.",
            )
        else:
            self.use_counter += 1
            #print(f"NewCounter:{self.use_counter}")

    def shoot_screen(self):
        self.original_pixmap = self.screen().grabWindow(0)

    def delete_oldest_content(self, dir_path: str):
        oldest_item = ""
        initial_path = dir_path
        if not os.path.exists(dir_path):
            print(f"Folder path not found : {dir_path}")
            return
        for item in os.listdir(initial_path):
            if oldest_item == "":
                oldest_item = item
            elif self.item_age_stripper(oldest_item) > self.item_age_stripper(item):
                oldest_item = item
        item_path = initial_path + "/" + oldest_item
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.remove(item_path)
            #Delete subfolders recursively, not properly implemented as of yet.
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        except Exception as e:
            print(f"Failed to delete {oldest_item}: {e}")
            return


    def item_age_stripper(self, itemName):
        #remove dashes, underscores and letters using regex
        item_age = re.sub(r"[-_\D]", "", itemName)
        return item_age

    def setOpacity(self, value: float):
        self.opacity_value = value

    def draw(self, painter: QPainter, rect: QRect):
        if self.original_pixmap is None:
            return
        painter.save()
        #print("painter ran")

        # Draw the pixelmap
        painter.setOpacity(self.opacity_value)
        painter.drawPixmap(rect, self.original_pixmap)
        #print(rect)
        painter.restore()