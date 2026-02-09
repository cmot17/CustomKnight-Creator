import os
import sys
import json

from spritehandler import spriteHandler
from PySide6 import QtGui, QtCore
from PySide6.QtWidgets import *
from pathlib import Path
from os import path, makedirs
from PIL import Image

from spritepacker_ui import Ui_MainWindow
from duplicatewizard_ui import Ui_Dialog

QtCore.QDir.addSearchPath("resources", "resources")


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.recoverSavedState()

    def addJSON(self, checked):
        fname = ""
        fname = QFileDialog.getExistingDirectory(
            self,
            'Select a base level animations folder (e.g. "Knight")',
            "c:\\",
            QFileDialog.Option.ShowDirsOnly,
        )
        fname += "/0.Atlases/SpriteInfo.json"
        # print("fname:")
        # print(fname)
        if fname != "/0.Atlases/SpriteInfo.json":
            if not self.listWidget.findItems(fname, QtCore.Qt.MatchFlag.MatchExactly):
                if self.listWidget.item(0) != None:
                    if str(Path(fname).parents[2]) == spriteHandler.basepath:
                        self.listWidget.addItem(
                            QListWidgetItem(str(Path(fname).parents[1]))
                        )
                        self.updateSavedState()
                    else:
                        warningMessage = QMessageBox.warning(
                            window,
                            "Inconsistent Base Path",
                            "Inconsistent Base Path:\nPlease make sure all of your top level sprite folders are in the same directory. (For example, the Knight and Spells Anim folders should be in the same folder)",
                        )
                else:
                    spriteHandler.basepath = str(Path(fname).parents[2])
                    # print("basepath:")
                    # print(spriteHandler.basepath)
                    self.listWidget.addItem(
                        QListWidgetItem(str(Path(fname).parents[1]))
                    )
                    self.updateSavedState()
            else:
                warningMessage = QMessageBox.warning(
                    window,
                    "Duplicate File Selected",
                    "Duplicate File Selected:\nPlease select a JSON file not already in the list",
                )

    def removeJSON(self, checked):
        self.listWidget.takeItem(self.listWidget.currentRow())
        self.updateSavedState()

    def enableCategory(self, checked):
        if self.listWidget_2.currentItem() != None:
            for category in self.listWidget_2.selectedItems():
                categoryID = category.text()
                spriteHandler.categories[categoryID] = True
            self.updateEnabled()
            # print(spriteHandler.categories)

    def disableCategory(self, checked):
        if self.listWidget_2.currentItem() != None:
            for category in self.listWidget_2.selectedItems():
                categoryID = category.text()
                spriteHandler.categories[categoryID] = False
            self.updateEnabled()
            # print(spriteHandler.categories)

    def loadCategories(self, checked):
        files = []
        for i in range(self.listWidget.count()):
            files.append(self.listWidget.item(i).text() + "/0.Atlases/SpriteInfo.json")
        # print(files)
        categories = spriteHandler.loadSpriteInfo(files)
        self.listWidget_2.clear()
        self.listWidget_2.addItems(categories)
        self.updateEnabled()
        self.infoBox.appendPlainText("Categories loaded.")

    def updateEnabled(self):
        greenBrush = QtGui.QBrush(
            QtCore.Qt.GlobalColor.green, QtCore.Qt.BrushStyle.Dense4Pattern
        )
        redBrush = QtGui.QBrush(
            QtCore.Qt.GlobalColor.red, QtCore.Qt.BrushStyle.Dense4Pattern
        )
        for item in spriteHandler.categories:
            if spriteHandler.categories[item]:
                self.listWidget_2.findItems(item, QtCore.Qt.MatchFlag.MatchExactly)[
                    0
                ].setBackground(greenBrush)
                self.listWidget_2.findItems(item, QtCore.Qt.MatchFlag.MatchExactly)[
                    0
                ].setIcon(
                    QtGui.QIcon(
                        os.path.abspath(
                            os.path.join(
                                os.path.dirname(__file__), "resources/checkicon.png"
                            )
                        )
                    )
                )
            else:
                self.listWidget_2.findItems(item, QtCore.Qt.MatchFlag.MatchExactly)[
                    0
                ].setBackground(redBrush)
                self.listWidget_2.findItems(item, QtCore.Qt.MatchFlag.MatchExactly)[
                    0
                ].setIcon(
                    QtGui.QIcon(
                        os.path.abspath(
                            os.path.join(
                                os.path.dirname(__file__), "resources/xicon.png"
                            )
                        )
                    )
                )
        self.updateSavedState()

    def loadAnimations(self, checked):
        animations = spriteHandler.loadAnimations("")
        self.listWidget_3.clear()
        self.listWidget_3.addItems(animations)
        self.listWidget_4.clear()
        self.listWidget_3.setCurrentRow(0)
        self.infoBox.appendPlainText("Animations loaded.")

    def animationChanged(self, current, previous):
        if current != None:
            self.listWidget_4.clear()
            self.listWidget_4.addItems(spriteHandler.loadSprites(current.text()))
            self.listWidget_4.setCurrentRow(0)

    def spriteChanged(self, current, previous):
        if current != None:
            path = next(x for x in spriteHandler.spritePath if current.text() in x)
            self.updatePreview(path)

    def packSprites(self, checked):
        if path.isdir(self.lineEdit.text()) and self.lineEdit.text() != "":
            spriteHandler.loadDuplicates("")
            completion = True
            for item in spriteHandler.duplicatesHashList:
                currentItem = item
                index = spriteHandler.duplicatesHashList.index(currentItem)
                sortedDuplicates = spriteHandler.sortByHash(index, currentItem)
                if not spriteHandler.checkCompletion(sortedDuplicates, currentItem):
                    completion = False
                    break
            if not completion:
                button = QMessageBox.warning(
                    window,
                    "Some duplicate sprites are not modified",
                    "Some duplicate sprites are not modified:\nThis means that a group of duplicates either is all vanilla, or the non-vanilla sprites do not match. You can continue if you intentionally left duplicate sprites different / vanilla. Would you like to continue packing?",
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
            self.filterAnimations()
            error = spriteHandler.packSprites(self.lineEdit.text())
            if error == False:
                QMessageBox.warning(
                    window,
                    "Error Writing Files",
                    "Error Writing Files:\nPlease make sure none of the output files are currently open",
                )
                self.infoBox.appendPlainText("Packing failed: file in use.")
            else:
                self.infoBox.appendPlainText("Done packing.")
            self.updateSavedState()
        else:
            QMessageBox.warning(
                window,
                "Invalid Output Path",
                "Invalid Output Path:\nPlease select a valid directory to output packed sprites into",
            )

    def chooseOutFolder(self, checked):
        dirname = QFileDialog.getExistingDirectory(
            self,
            "Select a folder to output packed sprites into",
            "c:\\",
            QFileDialog.Option.ShowDirsOnly,
        )
        self.lineEdit.setText(dirname)
        self.infoBox.appendPlainText("Output folder selected.")

    def updateOutputPath(self, newPath):
        # print("newpath:")
        # print(newPath)
        spriteHandler.savedOutputFolder = self.lineEdit.text()
        self.updateSavedState()

    def updatePreview(self, path):
        width = self.spritePreview.width()
        height = self.spritePreview.height()
        pixmap = QtGui.QPixmap(spriteHandler.basepath + "/" + path)
        # pixmap = pixmap.scaled(width, height, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.spritePreview.setPixmap(pixmap)
        self.spritePreview.setScaledContents(False)
        self.spritePreview.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def duplicateWizard(self, checked):
        self.infoBox.appendPlainText("Loading all duplicates...")
        self.infoBox.appendPlainText("(This might take a while)")
        self.infoBox.repaint()
        wizard = WizardDialog(self, obj=None, animation="")
        wizard.exec()

    def animationDuplicates(self, checked):
        if self.listWidget_3.currentItem() != None:
            self.infoBox.appendPlainText("Loading animation duplicates...")
            self.infoBox.repaint()
            selectedAnimation = str(self.listWidget_3.currentItem().text())
            self.animationFilter.setText("")
            self.filterAnimations()
            wizard = WizardDialog(self, obj=None, animation=selectedAnimation)
            wizard.exec()

    def updateAutoplay(self, value):
        if value == 2:
            if self.listWidget_4.item(0) != None:
                self.playAnimationButton.setEnabled(False)
                self.listWidget_4.setCurrentRow(0)
                QtCore.QTimer.singleShot(80, self.frameTimer)

    def playAnimation(self, checked):
        if self.listWidget_4.item(0) != None:
            if not self.autoplayAnimation.isChecked():
                self.playAnimationButton.setEnabled(False)
                self.listWidget_4.setCurrentRow(0)
                QtCore.QTimer.singleShot(80, self.frameTimer)

    def frameTimer(self):
        if self.listWidget_4.item(0) != None:
            # print("nextframe")
            if self.listWidget_4.currentRow() + 1 >= self.listWidget_4.count():
                self.listWidget_4.setCurrentRow(0)
                # print("restarted")
                if self.autoplayAnimation.isChecked():
                    QtCore.QTimer.singleShot(80, self.frameTimer)
                else:
                    self.playAnimationButton.setEnabled(True)
            else:
                # print("frame advanced")
                self.listWidget_4.setCurrentRow(self.listWidget_4.currentRow() + 1)
                QtCore.QTimer.singleShot(80, self.frameTimer)

    def filterAnimations(self):
        animations = spriteHandler.loadAnimations(self.animationFilter.text())
        self.listWidget_3.clear()
        self.listWidget_3.addItems(animations)
        self.listWidget_4.clear()
        self.listWidget_3.setCurrentRow(0)

    def recoverSavedState(self):
        savePath = path.join(
            path.expanduser("~"), "CustomKnight Creator", "savestate.json"
        )
        if not path.exists(path.dirname(savePath)):
            makedirs(path.dirname(savePath))
        Path(savePath).touch(exist_ok=True)
        saveFile = open(savePath, "r")
        # print(savePath)
        if path.getsize(savePath) != 0:
            saveData = json.load(saveFile)

            if saveData["openFolders"] != []:
                self.listWidget.addItems(saveData["openFolders"])
                spriteHandler.basepath = str(path.dirname(saveData["openFolders"][0]))
                # print("basepath:")
                # print(spriteHandler.basepath)
                self.loadCategories(False)
                for category in saveData["enabledCategories"]:
                    spriteHandler.categories[category] = saveData["enabledCategories"][
                        category
                    ]
                self.updateEnabled()
                self.loadAnimations(False)
            if saveData["outputFolder"] != "":
                # print("recovered output folder:")
                # print(saveData["outputFolder"])
                spriteHandler.savedOutputFolder = saveData["outputFolder"]
                self.lineEdit.setText(saveData["outputFolder"])

    def updateSavedState(self):
        items = [self.listWidget.item(x).text() for x in range(self.listWidget.count())]
        newState = json.dumps(
            {
                "openFolders": items,
                "enabledCategories": spriteHandler.categories,
                "outputFolder": spriteHandler.savedOutputFolder,
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
        )
        outputfile.write(newState)
        outputfile.close()


class WizardDialog(QDialog, Ui_Dialog):
    def __init__(self, *args, obj=None, **kwargs):
        super(WizardDialog, self).__init__()
        self.setupUi(self)
        animation = kwargs["animation"]
        # print(animation)
        spriteHandler.loadDuplicates(animation)
        self.duplicatesWidget.addItems(spriteHandler.duplicatesHashList)
        self.updateFrames(self.duplicatesWidget.currentItem(), None)
        self.updatePreview(self.listWidget.currentItem(), None)
        self.updateCompletion()

    def selectMainCopy(self, checked):
        if self.listWidget.currentItem() != None:
            spriteHandler.copyMain(str(self.listWidget.currentItem().text()))
            self.updateCompletion()
            window.infoBox.appendPlainText("Duplicates replaced with selected sprite.")

    def autoreplaceAll(self, check):
        if self.duplicatesWidget.count() != 0:
            for item in [
                self.duplicatesWidget.item(x).text()
                for x in range(self.duplicatesWidget.count())
            ]:
                print(item)
                timeSort = sorted(
                    [
                        spriteHandler.basepath + "/" + x
                        for x in spriteHandler.duplicatesList[
                            spriteHandler.duplicatesHashList.index(item)
                        ]
                    ],
                    key=path.getmtime,
                    reverse=True,
                )
                file = timeSort[0]
                i = spriteHandler.spritePath.index(
                    [x for x in spriteHandler.spritePath if x in file][0]
                )
                im = Image.open(file)
                im = im.crop(
                    (
                        spriteHandler.spriteXR[i],
                        im.size[1]
                        - spriteHandler.spriteYR[i]
                        - spriteHandler.spriteH[i],
                        spriteHandler.spriteXR[i] + spriteHandler.spriteW[i],
                        im.size[1] - spriteHandler.spriteYR[i],
                    )
                )
                imData = im.getdata()
                newHash = hash(tuple(map(tuple, imData)))
                print(file)
                if newHash != item:
                    spriteHandler.copyMain(spriteHandler.spritePath[i])
        self.updateCompletion()
        window.infoBox.appendPlainText(
            "All changed sprites have been copied to their duplicates."
        )

    def updatePreview(self, current, previous):
        if current != None:
            width = self.preview.width()
            height = self.preview.height()
            pixmap = QtGui.QPixmap(spriteHandler.basepath + "/" + str(current.text()))
            pixmap = pixmap.scaled(
                width, height, QtCore.Qt.AspectRatioMode.KeepAspectRatio
            )
            self.preview.setPixmap(pixmap)
            self.preview.setScaledContents(False)
            self.preview.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def updateFrames(self, current, previous):
        if current != None:
            self.listWidget.clear()
            currentItem = str(self.duplicatesWidget.currentItem().text())
            index = spriteHandler.duplicatesHashList.index(currentItem)
            sortedDuplicates = spriteHandler.sortByHash(index, currentItem)
            self.listWidget.addItems(sortedDuplicates)
            self.listWidget.setCurrentRow(0)

    def updateCompletion(self):
        greenBrush = QtGui.QBrush(
            QtCore.Qt.GlobalColor.green, QtCore.Qt.BrushStyle.Dense4Pattern
        )
        redBrush = QtGui.QBrush(
            QtCore.Qt.GlobalColor.red, QtCore.Qt.BrushStyle.Dense4Pattern
        )
        for item in [
            self.duplicatesWidget.item(x) for x in range(self.duplicatesWidget.count())
        ]:
            currentItem = item.text()
            index = spriteHandler.duplicatesHashList.index(currentItem)
            sortedDuplicates = spriteHandler.sortByHash(index, currentItem)
            if spriteHandler.checkCompletion(sortedDuplicates, currentItem):
                item.setBackground(greenBrush)
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
                item.setBackground(redBrush)
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
