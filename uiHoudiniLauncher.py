# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'houdini_launcheruSyIcX.ui'
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
        HoudiniLauncher.resize(696, 397)
        self.centralwidget = QWidget(HoudiniLauncher)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.launch_project = QPushButton(self.centralwidget)
        self.launch_project.setObjectName(u"launch_project")

        self.gridLayout_2.addWidget(self.launch_project, 1, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 2, 1, 1)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 2, 1, 1)

        self.projects_list = QComboBox(self.centralwidget)
        self.projects_list.setObjectName(u"projects_list")

        self.gridLayout.addWidget(self.projects_list, 1, 3, 1, 1)

        self.projects_location = QLineEdit(self.centralwidget)
        self.projects_location.setObjectName(u"projects_location")

        self.gridLayout.addWidget(self.projects_location, 0, 3, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 2, 3, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        HoudiniLauncher.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(HoudiniLauncher)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setEnabled(False)
        self.menubar.setGeometry(QRect(0, 0, 696, 20))
        HoudiniLauncher.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(HoudiniLauncher)
        self.statusbar.setObjectName(u"statusbar")
        HoudiniLauncher.setStatusBar(self.statusbar)

        self.retranslateUi(HoudiniLauncher)

        QMetaObject.connectSlotsByName(HoudiniLauncher)
    # setupUi

    def retranslateUi(self, HoudiniLauncher):
        HoudiniLauncher.setWindowTitle(QCoreApplication.translate("HoudiniLauncher", u"MainWindow", None))
        self.launch_project.setText(QCoreApplication.translate("HoudiniLauncher", u"Launch", None))
        self.label.setText(QCoreApplication.translate("HoudiniLauncher", u"Projects Location", None))
        self.label_2.setText(QCoreApplication.translate("HoudiniLauncher", u"Launch Project", None))
        self.projects_location.setText(QCoreApplication.translate("HoudiniLauncher", u"/media/white/projects", None))
    # retranslateUi

