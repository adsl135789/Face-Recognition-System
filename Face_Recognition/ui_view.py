# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_file/main.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import os
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 700)
        MainWindow.setMinimumSize(QtCore.QSize(1000, 700))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.left = QtWidgets.QWidget(self.centralwidget)
        self.left.setMinimumSize(QtCore.QSize(300, 600))
        self.left.setObjectName("left")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.left)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(self.left)
        self.widget.setObjectName("widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label1 = QtWidgets.QLabel(self.widget)
        self.label1.setMaximumSize(QtCore.QSize(16777215, 80))
        font = QtGui.QFont()
        font.setFamily("Uroob")
        font.setPointSize(52)
        font.setBold(False)
        font.setItalic(False)
        self.label1.setFont(font)
        self.label1.setStyleSheet("color: rgb(105, 183, 222);\n"
"font: 52pt \"Uroob\";")
        self.label1.setObjectName("label1")
        self.gridLayout_2.addWidget(self.label1, 1, 0, 1, 1)
        self.logo_label = QtWidgets.QLabel(self.widget)
        self.logo_label.setMinimumSize(QtCore.QSize(100, 100))
        self.logo_label.setMaximumSize(QtCore.QSize(100, 100))
        self.logo_label.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.logo_label.setText("")
        img_path = os.path.join(os.getcwd(), "icon/JINWEN.png")
        self.logo_label.setPixmap(QtGui.QPixmap(img_path))
        self.logo_label.setScaledContents(True)
        self.logo_label.setObjectName("logo_label")
        self.gridLayout_2.addWidget(self.logo_label, 1, 1, 1, 1)
        self.label2 = QtWidgets.QLabel(self.widget)
        self.label2.setMaximumSize(QtCore.QSize(16777215, 80))
        font = QtGui.QFont()
        font.setFamily("Uroob")
        font.setPointSize(50)
        font.setBold(False)
        font.setItalic(False)
        self.label2.setFont(font)
        self.label2.setStyleSheet("color: rgb(105, 183, 222);\n"
"font: 50pt \"Uroob\";")
        self.label2.setTextFormat(QtCore.Qt.RichText)
        self.label2.setObjectName("label2")
        self.gridLayout_2.addWidget(self.label2, 3, 0, 1, 2)
        self.verticalLayout.addWidget(self.widget)
        self.user_userWidget = QtWidgets.QWidget(self.left)
        self.user_userWidget.setMaximumSize(QtCore.QSize(16777215, 400))
        self.user_userWidget.setObjectName("user_userWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.user_userWidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.name_label = QtWidgets.QLabel(self.user_userWidget)
        self.name_label.setStyleSheet("font: 80 18pt \"OpenDyslexic\";\n"
"")
        self.name_label.setObjectName("name_label")
        self.verticalLayout_3.addWidget(self.name_label)
        self.name_content = QtWidgets.QLabel(self.user_userWidget)
        self.name_content.setMaximumSize(QtCore.QSize(16777215, 80))
        self.name_content.setStyleSheet("color: rgb(55, 67, 94);\n"
                                      "font: 80 18pt \"OpenDyslexic\";\n"
"")
        self.name_content.setText("")
        self.name_content.setObjectName("name_content")
        self.verticalLayout_3.addWidget(self.name_content)
        self.time_label = QtWidgets.QLabel(self.user_userWidget)
        self.time_label.setStyleSheet("font: 80 18pt \"OpenDyslexic\";\n"
"")
        self.time_label.setObjectName("time_label")
        self.verticalLayout_3.addWidget(self.time_label)
        self.time_content = QtWidgets.QLabel(self.user_userWidget)
        self.time_content.setMaximumSize(QtCore.QSize(16777215, 80))
        self.time_content.setStyleSheet("color: rgb(55, 67, 94);\n"
                                      "font: 80 18pt \"OpenDyslexic\";\n"
"")
        self.time_content.setText("")
        self.time_content.setObjectName("time_content")
        self.verticalLayout_3.addWidget(self.time_content)
        self.verticalLayout.addWidget(self.user_userWidget)
        self.leftWCFrame = QtWidgets.QFrame(self.left)
        self.leftWCFrame.setMinimumSize(QtCore.QSize(300, 300))
        self.leftWCFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.leftWCFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.leftWCFrame.setObjectName("leftWCFrame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.leftWCFrame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.left_labelWC = QtWidgets.QLabel(self.leftWCFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.left_labelWC.sizePolicy().hasHeightForWidth())
        self.left_labelWC.setSizePolicy(sizePolicy)
        self.left_labelWC.setMinimumSize(QtCore.QSize(300, 300))
        self.left_labelWC.setText("")
        self.left_labelWC.setObjectName("left_labelWC")
        self.horizontalLayout_2.addWidget(self.left_labelWC)
        self.verticalLayout.addWidget(self.leftWCFrame)
        self.horizontalLayout.addWidget(self.left)
        self.right = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(self.right.sizePolicy().hasHeightForWidth())
        self.right.setSizePolicy(sizePolicy)
        self.right.setMinimumSize(QtCore.QSize(600, 600))
        self.right.setMaximumSize(QtCore.QSize(2000, 2000))
        self.right.setObjectName("right")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.right)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.rightWCFrame = QtWidgets.QFrame(self.right)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(self.rightWCFrame.sizePolicy().hasHeightForWidth())
        self.rightWCFrame.setSizePolicy(sizePolicy)
        self.rightWCFrame.setMinimumSize(QtCore.QSize(600, 600))
        self.rightWCFrame.setMaximumSize(QtCore.QSize(2000, 2000))
        self.rightWCFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.rightWCFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.rightWCFrame.setObjectName("rightWCFrame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.rightWCFrame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.right_labelWC = QtWidgets.QLabel(self.rightWCFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(self.right_labelWC.sizePolicy().hasHeightForWidth())
        self.right_labelWC.setSizePolicy(sizePolicy)
        self.right_labelWC.setMinimumSize(QtCore.QSize(600, 600))
        self.right_labelWC.setText("")
        self.right_labelWC.setObjectName("right_labelWC")
        self.verticalLayout_2.addWidget(self.right_labelWC)
        self.verticalLayout_7.addWidget(self.rightWCFrame)
        self.horizontalLayout.addWidget(self.right)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label1.setText(_translate("MainWindow", "Face"))
        self.label2.setText(_translate("MainWindow", "Recognition"))
        self.name_label.setText(_translate("MainWindow", "Name"))
        self.time_label.setText(_translate("MainWindow", "Entry Time"))
