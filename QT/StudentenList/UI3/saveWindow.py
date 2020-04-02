# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui3\saveWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_saveWindow(object):
    def setupUi(self, saveWindow):
        saveWindow.setObjectName("saveWindow")
        saveWindow.resize(232, 262)
        saveWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.centralwidget = QtWidgets.QWidget(saveWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.studiengang = QtWidgets.QLineEdit(self.centralwidget)
        self.studiengang.setObjectName("studiengang")
        self.gridLayout.addWidget(self.studiengang, 2, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.name = QtWidgets.QLineEdit(self.centralwidget)
        self.name.setObjectName("name")
        self.gridLayout.addWidget(self.name, 1, 1, 1, 1)
        self.vName = QtWidgets.QLineEdit(self.centralwidget)
        self.vName.setObjectName("vName")
        self.gridLayout.addWidget(self.vName, 0, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 3, 0, 1, 1)
        saveWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(saveWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 232, 22))
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
        self.label_3.setText(_translate("saveWindow", "Studiengang"))
        self.label_2.setText(_translate("saveWindow", "Nachname"))
        self.label.setText(_translate("saveWindow", "Vorname"))
        self.pushButton.setText(_translate("saveWindow", "Speichern"))
