import os
from typing import Optional

from PIL import Image
from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import QDialog, QListWidgetItem

from duplicatewizard_ui import Ui_Dialog
from spritehandler import SpriteHandler

class WizardDialog(QDialog, Ui_Dialog):
    def __init__(self, animation: str) -> None:
        super().__init__()
        self.setupUi(self)
        self.connect_signals()
        SpriteHandler.load_duplicates(animation)
        self.duplicatesListWidget.addItems(SpriteHandler.duplicatesHashList)
        self.update_frames(self.duplicatesListWidget.currentItem(), None)
        self.update_preview(self.framesListWidget.currentItem(), None)
        self.update_completion()

    def connect_signals(self) -> None:
        self.duplicatesListWidget.currentItemChanged.connect(self.update_frames)
        self.framesListWidget.currentItemChanged.connect(self.update_preview)
        self.replaceButton.clicked.connect(self.select_main_copy)
        self.autoReplaceButton.clicked.connect(self.autoreplace_all)

    def select_main_copy(self) -> None:
        current_item = self.framesListWidget.currentItem()
        if current_item:
            SpriteHandler.copy_main(current_item.text())
            self.update_completion()

    def autoreplace_all(self) -> None:
        if self.duplicatesListWidget.count() != 0:
            for index in range(self.duplicatesListWidget.count()):
                item_text = self.duplicatesListWidget.item(index).text()
                index_in_list = SpriteHandler.duplicatesHashList.index(item_text)
                duplicates = SpriteHandler.duplicatesList[index_in_list]
                time_sorted = sorted(
                    [os.path.join(SpriteHandler.basepath, x) for x in duplicates],
                    key=os.path.getmtime,
                    reverse=True,
                )
                file = time_sorted[0]
                sprite_index = SpriteHandler.spritePath.index(
                    next((x for x in SpriteHandler.spritePath if x in file), "")
                )
                image = Image.open(file)
                image = image.crop(
                    (
                        SpriteHandler.spriteXR[sprite_index],
                        image.size[1]
                        - SpriteHandler.spriteYR[sprite_index]
                        - SpriteHandler.spriteH[sprite_index],
                        SpriteHandler.spriteXR[sprite_index] + SpriteHandler.spriteW[sprite_index],
                        image.size[1] - SpriteHandler.spriteYR[sprite_index],
                    )
                )
                image_data = image.getdata()
                new_hash = hash(tuple(map(tuple, image_data)))
                if new_hash != int(item_text):
                    SpriteHandler.copy_main(SpriteHandler.spritePath[sprite_index])
        self.update_completion()

    def update_preview(
        self, current: Optional[QListWidgetItem], _previous: Optional[QListWidgetItem]
    ) -> None:
        if current:
            pixmap = QtGui.QPixmap(os.path.join(SpriteHandler.basepath, current.text()))
            pixmap = pixmap.scaled(
                self.preview.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatio
            )
            self.preview.setPixmap(pixmap)
            self.preview.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def update_frames(
        self, current: Optional[QListWidgetItem], _previous: Optional[QListWidgetItem]
    ) -> None:
        if current:
            self.framesListWidget.clear()
            current_item = current.text()
            index = SpriteHandler.duplicatesHashList.index(current_item)
            sorted_duplicates = SpriteHandler.sort_by_hash(index, current_item)
            self.framesListWidget.addItems(sorted_duplicates)
            self.framesListWidget.setCurrentRow(0)

    def update_completion(self) -> None:
        green_brush = QtGui.QBrush(QtCore.Qt.GlobalColor.green)
        red_brush = QtGui.QBrush(QtCore.Qt.GlobalColor.red)
        for index in range(self.duplicatesListWidget.count()):
            item = self.duplicatesListWidget.item(index)
            current_item = item.text()
            index_in_list = SpriteHandler.duplicatesHashList.index(current_item)
            sorted_duplicates = SpriteHandler.sort_by_hash(index_in_list, current_item)
            is_complete = SpriteHandler.check_completion(sorted_duplicates, current_item)
            item.setBackground(green_brush if is_complete else red_brush)
            icon_path = "resources/checkicon.png" if is_complete else "resources/xicon.png"
            item.setIcon(QtGui.QIcon(icon_path))
