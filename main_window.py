import json
import os
from os import makedirs, path
from pathlib import Path
from typing import Optional, List

from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import (
    QFileDialog,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
)

from spritehandler import SpriteHandler
from spritepacker_ui import Ui_MainWindow
from wizard_dialog import WizardDialog


QtCore.QDir.addSearchPath("resources", "resources")

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.root_folders: List[Path] = []
        self.loaded_categories: List[str] = []
        self.base_path: Path = Path("")

        self.setupUi(self)
        self.connect_signals()
        self.recover_saved_state()

    def connect_signals(self) -> None:
        self.addRootFolderButton.clicked.connect(self.add_root_folder)
        self.removeRootFolderButton.clicked.connect(self.remove_root_folder)
        self.enableCategoryButton.clicked.connect(self.enable_category)
        self.disableCategoryButton.clicked.connect(self.disable_category)
        self.loadCategoriesButton.clicked.connect(self.load_categories)
        self.loadAnimationsButton.clicked.connect(self.load_animations)
        self.animationsListWidget.currentItemChanged.connect(self.animation_changed)
        self.spritesListWidget.currentItemChanged.connect(self.sprite_changed)
        self.packSpritesButton.clicked.connect(self.pack_sprites)
        self.chooseOutputFolderButton.clicked.connect(self.choose_out_folder)
        self.outputFolderLineEdit.textChanged.connect(self.update_output_path)
        self.duplicateWizardButton.clicked.connect(self.duplicate_wizard)
        self.animationDuplicatesButton.clicked.connect(self.animation_duplicates)
        self.autoplayAnimationCheckBox.stateChanged.connect(self.update_autoplay)
        self.playAnimationButton.clicked.connect(self.play_animation)
        self.animationFilterLineEdit.textChanged.connect(self.filter_animations)

    def add_root_folder(self) -> None:
        selected_path_str = QFileDialog.getExistingDirectory(
            self,
            'Select a base level animations folder (e.g. "Knight")',
            str(self.base_path.resolve() if self.base_path != Path("") else Path.home()),
            QFileDialog.Option.ShowDirsOnly,
        )
        if not selected_path_str:
            return

        selected_path = Path(selected_path_str)

        if selected_path in self.root_folders:
            QMessageBox.warning(
                self,
                "Duplicate Folder Selected",
                "This folder is already in the list.",
            )
            return

        if not self.root_folders:
            self.base_path = selected_path.parent
        elif selected_path.parent != self.base_path:
            QMessageBox.warning(
                self,
                "Inconsistent Base Path",
                "All top-level sprite folders must be in the same directory.",
            )
            return

        self.root_folders.append(selected_path)
        self.rootFoldersListWidget.addItem(QListWidgetItem(selected_path.name))
        self.update_saved_state()

    def remove_root_folder(self) -> None:
        current_item = self.rootFoldersListWidget.currentItem()
        if current_item:
            folder_name = current_item.text()
            folder_path = self.base_path / folder_name
            if folder_path in self.root_folders:
                self.root_folders.remove(folder_path)
                self.rootFoldersListWidget.takeItem(self.rootFoldersListWidget.currentRow())
                self.update_saved_state()

    def enable_category(self) -> None:
        for category_item in self.categoriesListWidget.selectedItems():
            category_id = category_item.text()
            SpriteHandler.categories[category_id] = True
        self.update_enabled()

    def disable_category(self) -> None:
        for category_item in self.categoriesListWidget.selectedItems():
            category_id = category_item.text()
            SpriteHandler.categories[category_id] = False
        self.update_enabled()

    def load_categories(self) -> None:
        sprite_info_paths = [folder / "0.Atlases/SpriteInfo.json" for folder in self.root_folders]
        self.loaded_categories = SpriteHandler.load_sprite_info(sprite_info_paths)
        self.categoriesListWidget.clear()
        self.categoriesListWidget.addItems(self.loaded_categories)
        self.update_enabled()
        self.infoBox.appendPlainText("Categories loaded.")

    def update_enabled(self) -> None:
        green_brush = QtGui.QBrush(QtCore.Qt.GlobalColor.green)
        red_brush = QtGui.QBrush(QtCore.Qt.GlobalColor.red)
        for category_name, is_enabled in SpriteHandler.categories.items():
            items = self.categoriesListWidget.findItems(category_name, QtCore.Qt.MatchFlag.MatchExactly)
            if items:
                item = items[0]
                item.setBackground(green_brush if is_enabled else red_brush)
                icon_path = "resources/checkicon.png" if is_enabled else "resources/xicon.png"
                item.setIcon(QtGui.QIcon(icon_path))
        self.update_saved_state()

    def load_animations(self) -> None:
        animations = SpriteHandler.load_animations("")
        self.animationsListWidget.clear()
        self.animationsListWidget.addItems(animations)
        self.spritesListWidget.clear()
        self.animationsListWidget.setCurrentRow(0)
        self.infoBox.appendPlainText("Animations loaded.")

    def animation_changed(
        self, current: Optional[QListWidgetItem], _previous: Optional[QListWidgetItem]
    ) -> None:
        if current:
            self.spritesListWidget.clear()
            sprites = SpriteHandler.load_sprites(current.text())
            self.spritesListWidget.addItems(sprites)
            self.spritesListWidget.setCurrentRow(0)

    def sprite_changed(
        self, current: Optional[QListWidgetItem], _previous: Optional[QListWidgetItem]
    ) -> None:
        if current:
            sprite_path = next((x for x in SpriteHandler.spritePath if current.text() in x), "")
            if sprite_path:
                self.update_preview(sprite_path)

    def pack_sprites(self) -> None:
        output_path = self.outputFolderLineEdit.text()
        if path.isdir(output_path) and output_path:
            SpriteHandler.load_duplicates("")
            incomplete = False
            for item in SpriteHandler.duplicatesHashList:
                index = SpriteHandler.duplicatesHashList.index(item)
                sorted_duplicates = SpriteHandler.sort_by_hash(index, item)
                if not SpriteHandler.check_completion(sorted_duplicates, item):
                    incomplete = True
                    break
            if incomplete:
                button = QMessageBox.warning(
                    self,
                    "Some duplicate sprites are not modified",
                    "Some duplicate sprites are not modified.\n"
                    "Continue packing?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    defaultButton=QMessageBox.StandardButton.No,
                )
                if button == QMessageBox.StandardButton.No:
                    self.infoBox.appendPlainText("Packing cancelled.")
                    self.infoBox.repaint()
                    return
            self.infoBox.appendPlainText("Packing sprites...")
            self.infoBox.repaint()
            self.animationFilterLineEdit.setText("")
            self.filter_animations()
            success = SpriteHandler.pack_sprites(output_path)
            if not success:
                QMessageBox.warning(
                    self,
                    "Error Writing Files",
                    "Please ensure none of the output files are open.",
                )
                self.infoBox.appendPlainText("Packing failed: file in use.")
            else:
                self.infoBox.appendPlainText("Done packing.")
            self.update_saved_state()
        else:
            QMessageBox.warning(
                self,
                "Invalid Output Path",
                "Please select a valid directory for output.",
            )

    def choose_out_folder(self) -> None:
        dirname = QFileDialog.getExistingDirectory(
            self,
            "Select a folder to output packed sprites into",
            "c:\\",
            QFileDialog.Option.ShowDirsOnly,
        )
        self.outputFolderLineEdit.setText(dirname)
        self.infoBox.appendPlainText("Output folder selected.")

    def update_output_path(self, _new_path: str) -> None:
        SpriteHandler.savedOutputFolder = self.outputFolderLineEdit.text()
        self.update_saved_state()

    def update_preview(self, new_path: str) -> None:
        pixmap = QtGui.QPixmap(os.path.join(SpriteHandler.basepath, new_path))
        self.spritePreview.setPixmap(pixmap)
        self.spritePreview.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def duplicate_wizard(self) -> None:
        self.infoBox.appendPlainText("Loading all duplicates...")
        self.infoBox.appendPlainText("(This might take a while)")
        self.infoBox.repaint()
        wizard = WizardDialog("")
        wizard.exec()

    def animation_duplicates(self) -> None:
        current_item = self.animationsListWidget.currentItem()
        if current_item:
            self.infoBox.appendPlainText("Loading animation duplicates...")
            self.infoBox.repaint()
            selected_animation = current_item.text()
            self.animationFilterLineEdit.setText("")
            self.filter_animations()
            wizard = WizardDialog(selected_animation)
            wizard.exec()

    def update_autoplay(self, value: int) -> None:
        if value == QtCore.Qt.CheckState.Checked.value:
            if self.spritesListWidget.item(0):
                self.playAnimationButton.setEnabled(False)
                self.spritesListWidget.setCurrentRow(0)
                QtCore.QTimer.singleShot(80, self.frame_timer)

    def play_animation(self) -> None:
        if self.spritesListWidget.item(0):
            if not self.autoplayAnimationCheckBox.isChecked():
                self.playAnimationButton.setEnabled(False)
                self.spritesListWidget.setCurrentRow(0)
                QtCore.QTimer.singleShot(80, self.frame_timer)

    def frame_timer(self) -> None:
        if self.spritesListWidget.item(0):
            current_row = self.spritesListWidget.currentRow()
            if current_row + 1 >= self.spritesListWidget.count():
                self.spritesListWidget.setCurrentRow(0)
                if self.autoplayAnimationCheckBox.isChecked():
                    QtCore.QTimer.singleShot(80, self.frame_timer)
                else:
                    self.playAnimationButton.setEnabled(True)
            else:
                self.spritesListWidget.setCurrentRow(current_row + 1)
                QtCore.QTimer.singleShot(80, self.frame_timer)

    def filter_animations(self) -> None:
        animations = SpriteHandler.load_animations(self.animationFilterLineEdit.text())
        self.animationsListWidget.clear()
        self.animationsListWidget.addItems(animations)
        self.spritesListWidget.clear()
        self.animationsListWidget.setCurrentRow(0)

    def recover_saved_state(self) -> None:
        save_path = path.join(
            path.expanduser("~"), "CustomKnight Creator", "savestate.json"
        )
        if not path.exists(path.dirname(save_path)):
            makedirs(path.dirname(save_path), exist_ok=True)

        if not path.exists(save_path):
            return

        with open(save_path, "r", encoding="utf-8") as save_file:
            if path.getsize(save_path) != 0:
                save_data = json.load(save_file)

                self.root_folders = [Path(folder) for folder in save_data.get("openFolders", [])]
                self.rootFoldersListWidget.addItems([folder.name for folder in self.root_folders])
                if self.root_folders:
                    self.base_path = self.root_folders[0].parent
                    self.load_categories()
                    SpriteHandler.categories.update(save_data.get("enabledCategories", {}))
                    self.update_enabled()
                    self.load_animations()
                output_folder = save_data.get("outputFolder", "")
                SpriteHandler.savedOutputFolder = output_folder
                self.outputFolderLineEdit.setText(output_folder)

    def update_saved_state(self) -> None:
        save_data = {
            "openFolders": [str(folder) for folder in self.root_folders],
            "enabledCategories": SpriteHandler.categories,
            "outputFolder": SpriteHandler.savedOutputFolder,
        }
        save_path = path.join(
            path.expanduser("~"), "CustomKnight Creator", "savestate.json"
        )
        makedirs(path.dirname(save_path), exist_ok=True)
        with open(save_path, "w", encoding="utf-8") as output_file:
            json.dump(save_data, output_file, indent=4)
