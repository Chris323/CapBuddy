import sys
from PySide6.QtCore import (QDir, QPoint, QRect, QStandardPaths, Qt)
from PySide6.QtGui import QImageWriter, QImageReader
from PySide6.QtWidgets import QFileDialog, QSizePolicy, QDialog, QMessageBox

class Screenshot():
    def save_screenshot(self):
        fmt = "png"  # In order to avoid shadowing built-in format
        initial_path = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.PicturesLocation)  # noqa: E501
        if not initial_path:
            initial_path = QDir.currentPath() + "/onion_stills"
        initial_path += f"/untitled.{fmt}"

        fileDialog = QFileDialog(self, "Save As", initial_path)
        fileDialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        fileDialog.setFileMode(QFileDialog.FileMode.AnyFile)
        fileDialog.setDirectory(initial_path)

        mime_types = []

        for bf in QImageWriter.supportedMimeTypes():
            mime_types.append(bf.data().decode("utf8"))
        fileDialog.setMimeTypeFilters(mime_types)
        fileDialog.selectMimeTypeFilter("image/" + fmt)
        fileDialog.setDefaultSuffix(fmt)
        if fileDialog.exec() != QDialog.DialogCode.Accepted:
            return

        #Attempts to save the file to file path
        file_name = fileDialog.selectedFiles()[0]
        if not self.original_pixmap.save(file_name):
            path = QDir.toNativeSeparators(file_name)
            QMessageBox.warning(
                self,
                "Save Error",
                f"The image could not be saved to {path}.",
            )

    def shoot_screen(self):
        self.original_pixmap = self.screen().grabWindow(0)
        self.new_screenshot_button.setDisabled(False)

    def update_current_screenshot(self):
        if self.original_pixmap.isNull():
            self.save_screenshot_button.setEnabled(False)
            self.screenshot_label.setText(f'Grabbing "{self.screen().name()}" failed.')
        else:
            self.save_screenshot_button.setEnabled(True)
            self.screenshot_label.setPixmap(
                self.original_pixmap.scaled(
                    self.screenshot_label.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )