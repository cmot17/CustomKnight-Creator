"""
Main file handling UI and assorted logic.
"""

import json
import os
import sys
from os import makedirs, path
from pathlib import Path
from typing import Optional

from PIL import Image
from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
)

from duplicatewizard_ui import Ui_Dialog
from spritehandler import SpriteHandler
from spritepacker_ui import Ui_MainWindow

QtCore.QDir.addSearchPath("resources", "resources")


class MainWindow(QMainWindow, Ui_MainWindow):

    rootFolders: list[Path] = []

    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.recover_saved_state()

    def add_root_folder(self) -> None:
        fname = ""
        fname = QFileDialog.getExistingDirectory(
            self,
            'Select a base level animations folder (e.g. "Knight")',
            "c:\\",
            QFileDialog.Option.ShowDirsOnly,
        )
        fname += "/0.Atlases/SpriteInfo.json"
        # print("fname: ")
        # print(fname)
        if fname != "/0.Atlases/SpriteInfo.json":
            if not self.listWidget.findItems(fname, QtCore.Qt.MatchFlag.MatchExactly):
                if self.listWidget.item(0) is not None:
                    if str(Path(fname).parents[2]) == SpriteHandler.basepath:
                        self.listWidget.addItem(
                            QListWidgetItem(str(Path(fname).parents[1]))
                        )
                        self.update_saved_state()
                    else:
                        QMessageBox.warning(
                            window,
                            "Inconsistent Base Path",
                            "Inconsistent Base Path:\n"
                            "Please make sure all of your top level sprite"
                            " folders are in the same directory."
                            "(For example, the Knight and Spells Anim"
                            " folders should be in the same folder)",
                        )
                else:
                    SpriteHandler.basepath = str(Path(fname).parents[2])
                    # print("basepath:")
                    # print(spriteHandler.basepath)
                    self.listWidget.addItem(
                        QListWidgetItem(str(Path(fname).parents[1]))
                    )
                    self.update_saved_state()
            else:
                QMessageBox.warning(
                    window,
                    "Duplicate File Selected",
                    "Duplicate File Selected:\nPlease select a JSON file not already in the list",
                )

    def remove_root_folder(self) -> None:
        self.listWidget.takeItem(self.listWidget.currentRow())
        self.update_saved_state()

    def enable_category(self) -> None:
        if self.listWidget_2.currentItem() is not None:
            for category in self.listWidget_2.selectedItems():
                category_id = category.text()
                SpriteHandler.categories[category_id] = True
            self.update_enabled()
            # print(spriteHandler.categories)

    def disable_category(self) -> None:
        if self.listWidget_2.currentItem() is not None:
            for category in self.listWidget_2.selectedItems():
                category_id = category.text()
                SpriteHandler.categories[category_id] = False
            self.update_enabled()
            # print(spriteHandler.categories)

    def load_categories(self) -> None:
        files = []
        for i in range(self.listWidget.count()):
            files.append(self.listWidget.item(i).text() + "/0.Atlases/SpriteInfo.json")
        # print(files)
        categories = SpriteHandler.load_sprite_info(files)
        self.listWidget_2.clear()
        self.listWidget_2.addItems(categories)
        self.update_enabled()
        self.infoBox.appendPlainText("Categories loaded.")

    def update_enabled(self) -> None:
        green_brush = QtGui.QBrush(
            QtCore.Qt.GlobalColor.green, QtCore.Qt.BrushStyle.Dense4Pattern
        )
        red_brush = QtGui.QBrush(
            QtCore.Qt.GlobalColor.red, QtCore.Qt.BrushStyle.Dense4Pattern
        )
        for category in SpriteHandler.categories.items():
            # category[0] is the category name and category[1] is the enabled status
            if category[1]:
                self.listWidget_2.findItems(
                    category[0], QtCore.Qt.MatchFlag.MatchExactly
                )[0].setBackground(green_brush)
                self.listWidget_2.findItems(
                    category[0], QtCore.Qt.MatchFlag.MatchExactly
                )[0].setIcon(
                    QtGui.QIcon(
                        os.path.abspath(
                            os.path.join(
                                os.path.dirname(__file__), "resources/checkicon.png"
                            )
                        )
                    )
                )
            else:
                self.listWidget_2.findItems(
                    category[0], QtCore.Qt.MatchFlag.MatchExactly
                )[0].setBackground(red_brush)
                self.listWidget_2.findItems(
                    category[0], QtCore.Qt.MatchFlag.MatchExactly
                )[0].setIcon(
                    QtGui.QIcon(
                        os.path.abspath(
                            os.path.join(
                                os.path.dirname(__file__), "resources/xicon.png"
                            )
                        )
                    )
                )
        self.update_saved_state()

    def load_animations(self) -> None:
        animations = SpriteHandler.load_animations("")
        self.listWidget_3.clear()
        self.listWidget_3.addItems(animations)
        self.listWidget_4.clear()
        self.listWidget_3.setCurrentRow(0)
        self.infoBox.appendPlainText("Animations loaded.")

    def animation_changed(
        self, current: Optional[QListWidgetItem], _previous: Optional[QListWidgetItem]
    ) -> None:
        if current is not None:
            self.listWidget_4.clear()
            self.listWidget_4.addItems(SpriteHandler.load_sprites(current.text()))
            self.listWidget_4.setCurrentRow(0)

    def sprite_changed(
        self, current: Optional[QListWidgetItem], _previous: Optional[QListWidgetItem]
    ) -> None:
        if current is not None:
            self.update_preview(
                next(x for x in SpriteHandler.spritePath if current.text() in x)
            )

    def pack_sprites(self) -> None:
        if path.isdir(self.lineEdit.text()) and self.lineEdit.text() != "":
            SpriteHandler.load_duplicates("")
            completion = True
            for item in SpriteHandler.duplicatesHashList:
                current_item = item
                index = SpriteHandler.duplicatesHashList.index(current_item)
                sorted_duplicates = SpriteHandler.sort_by_hash(index, current_item)
                if not SpriteHandler.check_completion(sorted_duplicates, current_item):
                    completion = False
                    break
            if not completion:
                button = QMessageBox.warning(
                    window,
                    "Some duplicate sprites are not modified",
                    "Some duplicate sprites are not modified:\n"
                    "This means that a group of duplicates either is all vanilla,"
                    "or the non-vanilla sprites do not match. "
                    "You can continue if you intentionally left duplicate sprites different / "
                    "vanilla. Would you like to continue packing?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    defaultButton=QMessageBox.StandardButton.No,
                )
                print(button)
                if button == QMessageBox.StandardButton.No:
                    self.infoBox.appendPlainText("Packing cancelled.")
                    self.infoBox.repaint()
                    return
            self.infoBox.appendPlainText("Packing sprites...")
            self.infoBox.repaint()
            self.animationFilter.setText("")
            self.filter_animations()
            error = SpriteHandler.pack_sprites(self.lineEdit.text())
            if not error:
                QMessageBox.warning(
                    window,
                    "Error Writing Files",
                    "Error Writing Files:\n"
                    "Please make sure none of the output files are currently open",
                )
                self.infoBox.appendPlainText("Packing failed: file in use.")
            else:
                self.infoBox.appendPlainText("Done packing.")
            self.update_saved_state()
        else:
            QMessageBox.warning(
                window,
                "Invalid Output Path",
                "Invalid Output Path:\n"
                "Please select a valid directory to output packed sprites into",
            )

    def choose_out_folder(self) -> None:
        dirname = QFileDialog.getExistingDirectory(
            self,
            "Select a folder to output packed sprites into",
            "c:\\",
            QFileDialog.Option.ShowDirsOnly,
        )
        self.lineEdit.setText(dirname)
        self.infoBox.appendPlainText("Output folder selected.")

    def update_output_path(self, _new_path: str) -> None:
        # print("newpath:")
        # print(new_path)
        SpriteHandler.savedOutputFolder = self.lineEdit.text()
        self.update_saved_state()

    def update_preview(self, new_path: str) -> None:
        # width = self.spritePreview.width()
        # height = self.spritePreview.height()
        pixmap = QtGui.QPixmap(SpriteHandler.basepath + "/" + new_path)
        # pixmap = pixmap.scaled(width, height, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.spritePreview.setPixmap(pixmap)
        self.spritePreview.setScaledContents(False)
        self.spritePreview.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def duplicate_wizard(self) -> None:
        self.infoBox.appendPlainText("Loading all duplicates...")
        self.infoBox.appendPlainText("(This might take a while)")
        self.infoBox.repaint()
        wizard = WizardDialog("")
        wizard.exec()

    def animation_duplicates(self) -> None:
        if self.listWidget_3.currentItem() is not None:
            self.infoBox.appendPlainText("Loading animation duplicates...")
            self.infoBox.repaint()
            selected_animation = str(self.listWidget_3.currentItem().text())
            self.animationFilter.setText("")
            self.filter_animations()
            wizard = WizardDialog(selected_animation)
            wizard.exec()

    def update_autoplay(self, value: int) -> None:
        if value == 2:
            if self.listWidget_4.item(0) is not None:
                self.playAnimationButton.setEnabled(False)
                self.listWidget_4.setCurrentRow(0)
                QtCore.QTimer.singleShot(80, self.frame_timer)

    def play_animation(self) -> None:
        if self.listWidget_4.item(0) is not None:
            if not self.autoplayAnimation.isChecked():
                self.playAnimationButton.setEnabled(False)
                self.listWidget_4.setCurrentRow(0)
                QtCore.QTimer.singleShot(80, self.frame_timer)

    def frame_timer(self) -> None:
        if self.listWidget_4.item(0) is not None:
            # print("nextframe")
            if self.listWidget_4.currentRow() + 1 >= self.listWidget_4.count():
                self.listWidget_4.setCurrentRow(0)
                # print("restarted")
                if self.autoplayAnimation.isChecked():
                    QtCore.QTimer.singleShot(80, self.frame_timer)
                else:
                    self.playAnimationButton.setEnabled(True)
            else:
                # print("frame advanced")
                self.listWidget_4.setCurrentRow(self.listWidget_4.currentRow() + 1)
                QtCore.QTimer.singleShot(80, self.frame_timer)

    def filter_animations(self) -> None:
        animations = SpriteHandler.load_animations(self.animationFilter.text())
        self.listWidget_3.clear()
        self.listWidget_3.addItems(animations)
        self.listWidget_4.clear()
        self.listWidget_3.setCurrentRow(0)

    def recover_saved_state(self) -> None:
        save_path = path.join(
            path.expanduser("~"), "CustomKnight Creator", "savestate.json"
        )
        if not path.exists(path.dirname(save_path)):
            makedirs(path.dirname(save_path))
        Path(save_path).touch(exist_ok=True)
        save_file = open(save_path, "r", encoding="utf-8")
        # print(savePath)
        if path.getsize(save_path) != 0:
            save_data = json.load(save_file)

            if save_data["openFolders"] != []:
                self.listWidget.addItems(save_data["openFolders"])
                SpriteHandler.basepath = str(path.dirname(save_data["openFolders"][0]))
                # print("basepath:")
                # print(spriteHandler.basepath)
                self.load_categories()
                for category in save_data["enabledCategories"]:
                    SpriteHandler.categories[category] = save_data["enabledCategories"][
                        category
                    ]
                self.update_enabled()
                self.load_animations()
            if save_data["outputFolder"] != "":
                # print("recovered output folder:")
                # print(saveData["outputFolder"])
                SpriteHandler.savedOutputFolder = save_data["outputFolder"]
                self.lineEdit.setText(save_data["outputFolder"])

    def update_saved_state(self) -> None:
        items = [self.listWidget.item(x).text() for x in range(self.listWidget.count())]
        new_state = json.dumps(
            {
                "openFolders": items,
                "enabledCategories": SpriteHandler.categories,
                "outputFolder": SpriteHandler.savedOutputFolder,
            }
        )
        # print("new savestate:")
        # print(newState)
        # print("current output path:")
        # print(spriteHandler.savedOutputFolder)
        # print(path.join(path.expanduser("~"), "CustomKnight Creator", "savestate.json"))
        outputfile = open(
            path.join(path.expanduser("~"), "CustomKnight Creator", "savestate.json"),
            "w",
            encoding="utf-8",
        )
        outputfile.write(new_state)
        outputfile.close()


class WizardDialog(QDialog, Ui_Dialog):
    def __init__(self, animation: str) -> None:
        super(WizardDialog, self).__init__()
        self.setupUi(self)
        # print(animation)
        SpriteHandler.load_duplicates(animation)
        self.duplicatesWidget.addItems(SpriteHandler.duplicatesHashList)
        self.update_frames(self.duplicatesWidget.currentItem(), None)
        self.update_preview(self.listWidget.currentItem(), None)
        self.update_completion()

    def select_main_copy(self) -> None:
        if self.listWidget.currentItem() is not None:
            SpriteHandler.copy_main(str(self.listWidget.currentItem().text()))
            self.update_completion()
            window.infoBox.appendPlainText("Duplicates replaced with selected sprite.")

    def autoreplace_all(self) -> None:
        if self.duplicatesWidget.count() != 0:
            for item in [
                self.duplicatesWidget.item(x).text()
                for x in range(self.duplicatesWidget.count())
            ]:
                print(item)
                time_sort = sorted(
                    [
                        SpriteHandler.basepath + "/" + x
                        for x in SpriteHandler.duplicatesList[
                            SpriteHandler.duplicatesHashList.index(item)
                        ]
                    ],
                    key=path.getmtime,
                    reverse=True,
                )
                file = time_sort[0]
                i = SpriteHandler.spritePath.index(
                    [x for x in SpriteHandler.spritePath if x in file][0]
                )
                image = Image.open(file)
                image = image.crop(
                    (
                        SpriteHandler.spriteXR[i],
                        image.size[1]
                        - SpriteHandler.spriteYR[i]
                        - SpriteHandler.spriteH[i],
                        SpriteHandler.spriteXR[i] + SpriteHandler.spriteW[i],
                        image.size[1] - SpriteHandler.spriteYR[i],
                    )
                )
                image_data = image.getdata()
                new_hash = hash(tuple(map(tuple, image_data)))
                print(file)
                if new_hash != item:
                    SpriteHandler.copy_main(SpriteHandler.spritePath[i])
        self.update_completion()
        window.infoBox.appendPlainText(
            "All changed sprites have been copied to their duplicates."
        )

    def update_preview(
        self, current: Optional[QListWidgetItem], _previous: Optional[QListWidgetItem]
    ) -> None:
        if current is not None:
            width = self.preview.width()
            height = self.preview.height()
            pixmap = QtGui.QPixmap(SpriteHandler.basepath + "/" + str(current.text()))
            pixmap = pixmap.scaled(
                width, height, QtCore.Qt.AspectRatioMode.KeepAspectRatio
            )
            self.preview.setPixmap(pixmap)
            self.preview.setScaledContents(False)
            self.preview.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def update_frames(
        self, current: Optional[QListWidgetItem], _previous: Optional[QListWidgetItem]
    ) -> None:
        if current is not None:
            self.listWidget.clear()
            current_item = str(self.duplicatesWidget.currentItem().text())
            index = SpriteHandler.duplicatesHashList.index(current_item)
            sorted_duplicates = SpriteHandler.sort_by_hash(index, current_item)
            self.listWidget.addItems(sorted_duplicates)
            self.listWidget.setCurrentRow(0)

    def update_completion(self) -> None:
        green_brush = QtGui.QBrush(
            QtCore.Qt.GlobalColor.green, QtCore.Qt.BrushStyle.Dense4Pattern
        )
        red_brush = QtGui.QBrush(
            QtCore.Qt.GlobalColor.red, QtCore.Qt.BrushStyle.Dense4Pattern
        )
        for item in [
            self.duplicatesWidget.item(x) for x in range(self.duplicatesWidget.count())
        ]:
            current_item = item.text()
            index = SpriteHandler.duplicatesHashList.index(current_item)
            sorted_duplicates = SpriteHandler.sort_by_hash(index, current_item)
            if SpriteHandler.check_completion(sorted_duplicates, current_item):
                item.setBackground(green_brush)
                item.setIcon(
                    QtGui.QIcon(
                        os.path.abspath(
                            os.path.join(
                                os.path.dirname(__file__), "resources/checkicon.png"
                            )
                        )
                    )
                )
            else:
                item.setBackground(red_brush)
                item.setIcon(
                    QtGui.QIcon(
                        os.path.abspath(
                            os.path.join(
                                os.path.dirname(__file__), "resources/xicon.png"
                            )
                        )
                    )
                )


app = QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()
