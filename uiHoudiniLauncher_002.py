# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'uiHoudiniLauncher_v002kFKuNK.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_HoudiniLauncher(object):
    def setupUi(self, HoudiniLauncher):
        if not HoudiniLauncher.objectName():
            HoudiniLauncher.setObjectName(u"HoudiniLauncher")
        HoudiniLauncher.resize(755, 584)
        self.centralwidget = QWidget(HoudiniLauncher)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.checkLoadFile = QCheckBox(self.centralwidget)
        self.checkLoadFile.setObjectName(u"checkLoadFile")

        self.gridLayout.addWidget(self.checkLoadFile, 2, 3, 1, 1)

        self.projects_location = QLineEdit(self.centralwidget)
        self.projects_location.setObjectName(u"projects_location")

        self.gridLayout.addWidget(self.projects_location, 0, 3, 1, 1)

        self.shotsList = QComboBox(self.centralwidget)
        self.shotsList.setObjectName(u"shotsList")

        self.gridLayout.addWidget(self.shotsList, 4, 3, 1, 1)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label, 0, 2, 1, 1)

        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_5, 4, 2, 1, 1)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_2, 1, 2, 1, 1)

        self.treeViewShots = QTreeView(self.centralwidget)
        self.treeViewShots.setObjectName(u"treeViewShots")
        self.treeViewShots.header().setMinimumSectionSize(200)
        self.treeViewShots.header().setDefaultSectionSize(300)

        self.gridLayout.addWidget(self.treeViewShots, 5, 3, 1, 1)

        self.projects_list = QComboBox(self.centralwidget)
        self.projects_list.setObjectName(u"projects_list")

        self.gridLayout.addWidget(self.projects_list, 1, 3, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 7, 3, 1, 1)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_3, 5, 2, 1, 1)

        self.tasksList = QComboBox(self.centralwidget)
        self.tasksList.setObjectName(u"tasksList")

        self.gridLayout.addWidget(self.tasksList, 3, 3, 1, 1)

        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_6, 3, 2, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.launch_project = QPushButton(self.centralwidget)
        self.launch_project.setObjectName(u"launch_project")
        self.launch_project.setMaximumSize(QSize(100, 16777215))
        self.launch_project.setLayoutDirection(Qt.RightToLeft)

        self.gridLayout_2.addWidget(self.launch_project, 2, 0, 1, 1)

        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 110))
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setLineWidth(0)
        self.checkDefaultEnv = QCheckBox(self.frame)
        self.checkDefaultEnv.setObjectName(u"checkDefaultEnv")
        self.checkDefaultEnv.setGeometry(QRect(10, 30, 85, 21))
        self.checkDefaultEnv.setChecked(True)
        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 10, 121, 16))
        self.checkProjectEnv = QCheckBox(self.frame)
        self.checkProjectEnv.setObjectName(u"checkProjectEnv")
        self.checkProjectEnv.setGeometry(QRect(10, 60, 151, 21))
        self.checkProjectEnv.setChecked(True)
        self.checkWowsEnv = QCheckBox(self.frame)
        self.checkWowsEnv.setObjectName(u"checkWowsEnv")
        self.checkWowsEnv.setGeometry(QRect(140, 30, 85, 21))
        self.checkOrcEnv = QCheckBox(self.frame)
        self.checkOrcEnv.setObjectName(u"checkOrcEnv")
        self.checkOrcEnv.setGeometry(QRect(140, 60, 85, 21))
        self.checkShEnv = QCheckBox(self.frame)
        self.checkShEnv.setObjectName(u"checkShEnv")
        self.checkShEnv.setGeometry(QRect(230, 30, 85, 21))

        self.gridLayout_2.addWidget(self.frame, 1, 0, 1, 1)

        HoudiniLauncher.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(HoudiniLauncher)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setEnabled(False)
        self.menubar.setGeometry(QRect(0, 0, 755, 20))
        HoudiniLauncher.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(HoudiniLauncher)
        self.statusbar.setObjectName(u"statusbar")
        HoudiniLauncher.setStatusBar(self.statusbar)

        self.retranslateUi(HoudiniLauncher)

        QMetaObject.connectSlotsByName(HoudiniLauncher)
    # setupUi

    def retranslateUi(self, HoudiniLauncher):
        HoudiniLauncher.setWindowTitle(QCoreApplication.translate("HoudiniLauncher", u"MainWindow", None))
        self.checkLoadFile.setText(QCoreApplication.translate("HoudiniLauncher", u"Load scene file", None))
        self.projects_location.setText(QCoreApplication.translate("HoudiniLauncher", u"/500GB_HDD_01/projects/my_daily_projects", None))
        self.label.setText(QCoreApplication.translate("HoudiniLauncher", u"Projects Location", None))
        self.label_5.setText(QCoreApplication.translate("HoudiniLauncher", u"File", None))
        self.label_2.setText(QCoreApplication.translate("HoudiniLauncher", u"Launch Project", None))
        self.label_3.setText(QCoreApplication.translate("HoudiniLauncher", u"Shots Browser", None))
        self.label_6.setText(QCoreApplication.translate("HoudiniLauncher", u"Task", None))
        self.launch_project.setText(QCoreApplication.translate("HoudiniLauncher", u"Launch", None))
        self.checkDefaultEnv.setText(QCoreApplication.translate("HoudiniLauncher", u"Default", None))
        self.label_4.setText(QCoreApplication.translate("HoudiniLauncher", u"Load environment", None))
        self.checkProjectEnv.setText(QCoreApplication.translate("HoudiniLauncher", u"Project specific", None))
        self.checkWowsEnv.setText(QCoreApplication.translate("HoudiniLauncher", u"WOWS", None))
        self.checkOrcEnv.setText(QCoreApplication.translate("HoudiniLauncher", u"ORC", None))
        self.checkShEnv.setText(QCoreApplication.translate("HoudiniLauncher", u"SH", None))
    # retranslateUi

