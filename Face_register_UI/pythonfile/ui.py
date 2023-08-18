import os,sys
from PyQt5 import Qtcore, QtWidgets, QtCore

from mainWindow import Ui_MainWindow as main_ui
from addUser import Ui_RegisiterWindow as register_ui
from addSupervisior import Ui_RegistierWindow as super_ui
from removeUser import Ui_MainWindow as remove_ui
from confirm import Ui_MainWindow as confirm_ui


class MainWindow(QtWidgets, QMainWindow, main_ui):
	switch_registerWindow = Qtcore.pyqtSingal()
	switch_supervisiorWindow = Qtcore.pyqtSingal()
	switch_removeWindow = Qtcore.pyqtSingal()

	def __init__(self):
		super(MainWindow, self).__init__()
		self.setupUi(self)
		self.regisiterButton.clicked.connect(self.goRegisiter)
        self.addSupurButton.clicked.connect(self.goSuper)
        self.removeButton.clicked.connect(self.goSuper)
    def goRegisiter(self):
    	self.switch_registerWindow.emit()
    def goSuper(self):
    	self.switch_supervisiorWindow.emit()
    def goRemove(self):
    	self.switch_removeWindow.emit()

	pass


class RegisterWindow(QtWidgets, QMainWindow, main_ui):
	def __init__(self):
		super(RegisterWindow, self).__init__()
		self.setupUi(self)
	pass



class SupervisiorWindow(QtWidgets, QMainWindow, main_ui):
	def __init__(self):
		super(SupervisiorWindow, self).__init__()
		self.setupUi(self)
	pass



class RemoveWindow(QtWidgets, QMainWindow, main_ui):
	def __init__(self):
		super(RemoveWindow, self).__init__()
		self.setupUi(self)
	pass



class ConfirmWindow(QtWidgets, QMainWindow, main_ui):
	def __init__(self):
		super(ConfirmWindow, self).__init__()
		self.setupUi(self)
	pass


class Controlloer:
	def __init__(self):
		pass
	def 
