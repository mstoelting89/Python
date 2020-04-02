# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(362, 267)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayout = QtWidgets.QFormLayout(self.centralwidget)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.label)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.weight = QtWidgets.QSpinBox(self.centralwidget)
        self.weight.setObjectName("weight")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.weight)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setTextFormat(QtCore.Qt.PlainText)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.height = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.height.setMaximum(2.5)
        self.height.setSingleStep(0.01)
        self.height.setObjectName("height")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.height)
        self.calculate = QtWidgets.QPushButton(self.centralwidget)
        self.calculate.setObjectName("calculate")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.calculate)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.result = QtWidgets.QLabel(self.centralwidget)
        self.result.setText("")
        self.result.setObjectName("result")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.result)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 362, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "BMI - Rechner"))
        self.label_2.setText(_translate("MainWindow", "Gewicht in kg"))
        self.label_3.setText(_translate("MainWindow", "Körpergröße in m"))
        self.calculate.setText(_translate("MainWindow", "BMI Berechnen!"))
        self.label_4.setText(_translate("MainWindow", "Dein BMI lautet: "))
