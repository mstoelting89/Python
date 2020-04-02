# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NewEntry\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_saveWindow(object):
    def setupUi(self, saveWindow):
        saveWindow.setObjectName("saveWindow")
        saveWindow.resize(216, 186)
        self.centralwidget = QtWidgets.QWidget(saveWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.vName = QtWidgets.QLabel(self.centralwidget)
        self.vName.setObjectName("vName")
        self.gridLayout.addWidget(self.vName, 1, 0, 1, 1)
        self.sGang = QtWidgets.QLabel(self.centralwidget)
        self.sGang.setObjectName("sGang")
        self.gridLayout.addWidget(self.sGang, 2, 0, 1, 1)
        self.Vorname = QtWidgets.QLineEdit(self.centralwidget)
        self.Vorname.setObjectName("Vorname")
        self.gridLayout.addWidget(self.Vorname, 1, 1, 1, 1)
        self.Studiengang = QtWidgets.QLineEdit(self.centralwidget)
        self.Studiengang.setObjectName("Studiengang")
        self.gridLayout.addWidget(self.Studiengang, 2, 1, 1, 1)
        self.nName = QtWidgets.QLabel(self.centralwidget)
        self.nName.setObjectName("nName")
        self.gridLayout.addWidget(self.nName, 0, 0, 1, 1)
        self.Nachname = QtWidgets.QLineEdit(self.centralwidget)
        self.Nachname.setObjectName("Nachname")
        self.gridLayout.addWidget(self.Nachname, 0, 1, 1, 1)
        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setObjectName("saveButton")
        self.gridLayout.addWidget(self.saveButton, 3, 0, 1, 1)
        self.cancelButton = QtWidgets.QPushButton(self.centralwidget)
        self.cancelButton.setObjectName("cancelButton")
        self.gridLayout.addWidget(self.cancelButton, 3, 1, 1, 1)
        saveWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(saveWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 216, 22))
        self.menubar.setObjectName("menubar")
        saveWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(saveWindow)
        self.statusbar.setObjectName("statusbar")
        saveWindow.setStatusBar(self.statusbar)

        self.retranslateUi(saveWindow)
        QtCore.QMetaObject.connectSlotsByName(saveWindow)

    def retranslateUi(self, saveWindow):
        _translate = QtCore.QCoreApplication.translate
        saveWindow.setWindowTitle(_translate("saveWindow", "MainWindow"))
        self.vName.setText(_translate("saveWindow", "Vorname"))
        self.sGang.setText(_translate("saveWindow", "Studiengang"))
        self.nName.setText(_translate("saveWindow", "Name"))
        self.saveButton.setText(_translate("saveWindow", "Speichern"))
        self.cancelButton.setText(_translate("saveWindow", "Abbrechen"))
