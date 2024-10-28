# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'spritepacker.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QHBoxLayout,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QMainWindow, QPlainTextEdit, QPushButton, QSizePolicy,
    QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1022, 642)
        icon = QIcon()
        icon.addFile(u":/main/SheoIcon.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_9 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")

        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.rootFoldersListWidget = QListWidget(self.centralwidget)
        self.rootFoldersListWidget.setObjectName(u"rootFoldersListWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rootFoldersListWidget.sizePolicy().hasHeightForWidth())
        self.rootFoldersListWidget.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.rootFoldersListWidget)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.addRootFolderButton = QPushButton(self.centralwidget)
        self.addRootFolderButton.setObjectName(u"addRootFolderButton")

        self.horizontalLayout_6.addWidget(self.addRootFolderButton)

        self.removeRootFolderButton = QPushButton(self.centralwidget)
        self.removeRootFolderButton.setObjectName(u"removeRootFolderButton")

        self.horizontalLayout_6.addWidget(self.removeRootFolderButton)

        self.loadCategoriesButton = QPushButton(self.centralwidget)
        self.loadCategoriesButton.setObjectName(u"loadCategoriesButton")

        self.horizontalLayout_6.addWidget(self.loadCategoriesButton)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.categoriesListWidget = QListWidget(self.centralwidget)
        self.categoriesListWidget.setObjectName(u"categoriesListWidget")
        sizePolicy.setHeightForWidth(self.categoriesListWidget.sizePolicy().hasHeightForWidth())
        self.categoriesListWidget.setSizePolicy(sizePolicy)
        self.categoriesListWidget.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        self.horizontalLayout_2.addWidget(self.categoriesListWidget)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.enableCategoryButton = QPushButton(self.centralwidget)
        self.enableCategoryButton.setObjectName(u"enableCategoryButton")

        self.horizontalLayout_7.addWidget(self.enableCategoryButton)

        self.disableCategoryButton = QPushButton(self.centralwidget)
        self.disableCategoryButton.setObjectName(u"disableCategoryButton")

        self.horizontalLayout_7.addWidget(self.disableCategoryButton)

        self.loadAnimationsButton = QPushButton(self.centralwidget)
        self.loadAnimationsButton.setObjectName(u"loadAnimationsButton")

        self.horizontalLayout_7.addWidget(self.loadAnimationsButton)


        self.verticalLayout.addLayout(self.horizontalLayout_7)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout.addWidget(self.label_4)

        self.infoBox = QPlainTextEdit(self.centralwidget)
        self.infoBox.setObjectName(u"infoBox")
        self.infoBox.setAcceptDrops(True)
        self.infoBox.setUndoRedoEnabled(False)
        self.infoBox.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.infoBox.setReadOnly(True)

        self.verticalLayout.addWidget(self.infoBox)


        self.horizontalLayout_9.addLayout(self.verticalLayout)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.verticalLayout_4.addWidget(self.label)

        self.spritePreview = QLabel(self.centralwidget)
        self.spritePreview.setObjectName(u"spritePreview")
        sizePolicy.setHeightForWidth(self.spritePreview.sizePolicy().hasHeightForWidth())
        self.spritePreview.setSizePolicy(sizePolicy)
        self.spritePreview.setMinimumSize(QSize(0, 268))

        self.verticalLayout_4.addWidget(self.spritePreview)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.animationDuplicatesButton = QPushButton(self.centralwidget)
        self.animationDuplicatesButton.setObjectName(u"animationDuplicatesButton")

        self.horizontalLayout_8.addWidget(self.animationDuplicatesButton)

        self.duplicateWizardButton = QPushButton(self.centralwidget)
        self.duplicateWizardButton.setObjectName(u"duplicateWizardButton")

        self.horizontalLayout_8.addWidget(self.duplicateWizardButton)

        self.playAnimationButton = QPushButton(self.centralwidget)
        self.playAnimationButton.setObjectName(u"playAnimationButton")
        self.playAnimationButton.setEnabled(True)
        self.playAnimationButton.setFlat(False)

        self.horizontalLayout_8.addWidget(self.playAnimationButton)

        self.autoplayAnimationCheckBox = QCheckBox(self.centralwidget)
        self.autoplayAnimationCheckBox.setObjectName(u"autoplayAnimationCheckBox")

        self.horizontalLayout_8.addWidget(self.autoplayAnimationCheckBox)


        self.verticalLayout_4.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_3.addWidget(self.label_5)

        self.animationFilterLineEdit = QLineEdit(self.centralwidget)
        self.animationFilterLineEdit.setObjectName(u"animationFilterLineEdit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.animationFilterLineEdit.sizePolicy().hasHeightForWidth())
        self.animationFilterLineEdit.setSizePolicy(sizePolicy1)
        self.animationFilterLineEdit.setClearButtonEnabled(True)

        self.verticalLayout_3.addWidget(self.animationFilterLineEdit)

        self.animationsListWidget = QListWidget(self.centralwidget)
        self.animationsListWidget.setObjectName(u"animationsListWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.animationsListWidget.sizePolicy().hasHeightForWidth())
        self.animationsListWidget.setSizePolicy(sizePolicy2)
        self.animationsListWidget.setMinimumSize(QSize(0, 145))

        self.verticalLayout_3.addWidget(self.animationsListWidget)


        self.horizontalLayout_3.addLayout(self.verticalLayout_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_2.addWidget(self.label_6)

        self.spritesListWidget = QListWidget(self.centralwidget)
        self.spritesListWidget.setObjectName(u"spritesListWidget")
        sizePolicy2.setHeightForWidth(self.spritesListWidget.sizePolicy().hasHeightForWidth())
        self.spritesListWidget.setSizePolicy(sizePolicy2)

        self.verticalLayout_2.addWidget(self.spritesListWidget)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.packSpritesButton = QPushButton(self.centralwidget)
        self.packSpritesButton.setObjectName(u"packSpritesButton")

        self.horizontalLayout_5.addWidget(self.packSpritesButton)

        self.chooseOutputFolderButton = QPushButton(self.centralwidget)
        self.chooseOutputFolderButton.setObjectName(u"chooseOutputFolderButton")

        self.horizontalLayout_5.addWidget(self.chooseOutputFolderButton)

        self.outputFolderLineEdit = QLineEdit(self.centralwidget)
        self.outputFolderLineEdit.setObjectName(u"outputFolderLineEdit")

        self.horizontalLayout_5.addWidget(self.outputFolderLineEdit)


        self.verticalLayout_4.addLayout(self.horizontalLayout_5)


        self.horizontalLayout_9.addLayout(self.verticalLayout_4)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.addRootFolderButton.clicked.connect(MainWindow.add_root_folder)
        self.removeRootFolderButton.clicked.connect(MainWindow.remove_root_folder)
        self.enableCategoryButton.clicked.connect(MainWindow.enable_category)
        self.disableCategoryButton.clicked.connect(MainWindow.disable_category)
        self.loadCategoriesButton.clicked.connect(MainWindow.load_categories)
        self.loadAnimationsButton.clicked.connect(MainWindow.load_animations)
        self.animationsListWidget.currentItemChanged.connect(MainWindow.animation_changed)
        self.spritesListWidget.currentItemChanged.connect(MainWindow.sprite_changed)
        self.packSpritesButton.clicked.connect(MainWindow.pack_sprites)
        self.chooseOutputFolderButton.clicked.connect(MainWindow.choose_out_folder)
        self.duplicateWizardButton.clicked.connect(MainWindow.duplicate_wizard)
        self.animationDuplicatesButton.clicked.connect(MainWindow.animation_duplicates)
        self.playAnimationButton.clicked.connect(MainWindow.play_animation)
        self.animationFilterLineEdit.textChanged.connect(MainWindow.filter_animations)
        self.outputFolderLineEdit.textChanged.connect(MainWindow.update_output_path)
        self.autoplayAnimationCheckBox.stateChanged.connect(MainWindow.update_autoplay)

        self.playAnimationButton.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"CustomKnight Creator", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">Root Folders</span></p></body></html>", None))
        self.addRootFolderButton.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.removeRootFolderButton.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
        self.loadCategoriesButton.setText(QCoreApplication.translate("MainWindow", u"Load Categories", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">Atlases / Collections</span></p></body></html>", None))
        self.enableCategoryButton.setText(QCoreApplication.translate("MainWindow", u"Enable", None))
        self.disableCategoryButton.setText(QCoreApplication.translate("MainWindow", u"Disable", None))
        self.loadAnimationsButton.setText(QCoreApplication.translate("MainWindow", u"Load Animations", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">Info</span></p></body></html>", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">Preview</span></p></body></html>", None))
        self.spritePreview.setText("")
        self.animationDuplicatesButton.setText(QCoreApplication.translate("MainWindow", u"View Animation Duplicate Groups", None))
        self.duplicateWizardButton.setText(QCoreApplication.translate("MainWindow", u"View All Duplicate Groups", None))
        self.playAnimationButton.setText(QCoreApplication.translate("MainWindow", u"Play Animation", None))
        self.autoplayAnimationCheckBox.setText(QCoreApplication.translate("MainWindow", u"Autoplay", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">Animations</span></p></body></html>", None))
        self.animationFilterLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Filter animations", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">Sprites</span></p></body></html>", None))
        self.packSpritesButton.setText(QCoreApplication.translate("MainWindow", u"Pack!", None))
        self.chooseOutputFolderButton.setText(QCoreApplication.translate("MainWindow", u"Select Output Folder", None))
        self.outputFolderLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Output folder path", None))
    # retranslateUi

