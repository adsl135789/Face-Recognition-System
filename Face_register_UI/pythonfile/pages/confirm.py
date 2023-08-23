# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/comfirm.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(518, 708)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setObjectName("gridLayout")
        self.label_1 = QtWidgets.QLabel(self.widget)
        self.label_1.setMaximumSize(QtCore.QSize(16777215, 70))
        font = QtGui.QFont()
        font.setFamily("Uroob")
        font.setPointSize(52)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_1.setFont(font)
        self.label_1.setStyleSheet("color: rgb(105, 183, 222);\n"
"font: 52pt \"Uroob\";")
        self.label_1.setObjectName("label_1")
        self.gridLayout.addWidget(self.label_1, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 80))
        font = QtGui.QFont()
        font.setFamily("Uroob")
        font.setPointSize(50)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(105, 183, 222);\n"
"font: 50pt \"Uroob\";")
        self.label_2.setTextFormat(QtCore.Qt.RichText)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.returnButton = QtWidgets.QPushButton(self.widget)
        self.returnButton.setMaximumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setFamily("OpenDyslexic")
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(10)
        font.setKerning(True)
        self.returnButton.setFont(font)
        self.returnButton.setStyleSheet("QPushButton {\n"
"    font: 80 18pt \"OpenDyslexic\";\n"
"    background-color: rgb(104, 140, 183);\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: rgba(59, 84, 120, 0);\n"
"    padding: 4px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(127, 182, 187);\n"
"        transform: tranlateY(-2px)\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    \n"
"    background-color: rgb(69, 69, 69);\n"
"    transfomr: translateY(0px)\n"
"}\n"
"")
        self.returnButton.setCheckable(False)
        self.returnButton.setObjectName("returnButton")
        self.gridLayout.addWidget(self.returnButton, 1, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addWidget(self.widget, 0, QtCore.Qt.AlignTop)
        self.webcamFrame = QtWidgets.QFrame(self.centralwidget)
        self.webcamFrame.setMinimumSize(QtCore.QSize(500, 500))
        self.webcamFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.webcamFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.webcamFrame.setObjectName("webcamFrame")
        self.verticalLayout.addWidget(self.webcamFrame)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_1.setText(_translate("MainWindow", "Confirm"))
        self.label_2.setText(_translate("MainWindow", "Supervisior"))
        self.returnButton.setText(_translate("MainWindow", "Main page"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())