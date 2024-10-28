# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'duplicatewizard.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)
import resources_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1058, 609)
        icon = QIcon()
        icon.addFile(u":/main/SheoIcon.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        Dialog.setWindowIcon(icon)
        self.horizontalLayout_2 = QHBoxLayout(Dialog)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.duplicatesListWidget = QListWidget(Dialog)
        self.duplicatesListWidget.setObjectName(u"duplicatesListWidget")
        self.duplicatesListWidget.setMinimumSize(QSize(151, 0))

        self.verticalLayout_2.addWidget(self.duplicatesListWidget)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_3.addWidget(self.label_2)

        self.framesListWidget = QListWidget(Dialog)
        self.framesListWidget.setObjectName(u"framesListWidget")
        self.framesListWidget.setMinimumSize(QSize(151, 0))

        self.verticalLayout_3.addWidget(self.framesListWidget)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.preview = QLabel(Dialog)
        self.preview.setObjectName(u"preview")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.preview.sizePolicy().hasHeightForWidth())
        self.preview.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.preview)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.replaceButton = QPushButton(Dialog)
        self.replaceButton.setObjectName(u"replaceButton")

        self.horizontalLayout.addWidget(self.replaceButton)

        self.autoReplaceButton = QPushButton(Dialog)
        self.autoReplaceButton.setObjectName(u"autoReplaceButton")

        self.horizontalLayout.addWidget(self.autoReplaceButton)

        self.finishButton = QPushButton(Dialog)
        self.finishButton.setObjectName(u"finishButton")

        self.horizontalLayout.addWidget(self.finishButton)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.horizontalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(Dialog)
        self.replaceButton.clicked.connect(Dialog.select_main_copy)
        self.finishButton.clicked.connect(Dialog.accept)
        self.framesListWidget.currentItemChanged.connect(Dialog.update_preview)
        self.duplicatesListWidget.currentItemChanged.connect(Dialog.update_frames)
        self.autoReplaceButton.clicked.connect(Dialog.autoreplace_all)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Duplicate Sprite Manager", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">Duplicate Groups</span></p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">Frames</span></p></body></html>", None))
        self.preview.setText("")
        self.replaceButton.setText(QCoreApplication.translate("Dialog", u"Select Main Copy", None))
        self.autoReplaceButton.setText(QCoreApplication.translate("Dialog", u"Autoreplace All", None))
        self.finishButton.setText(QCoreApplication.translate("Dialog", u"Finish", None))
    # retranslateUi

