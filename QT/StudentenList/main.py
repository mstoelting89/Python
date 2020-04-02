import sys
import csv
from qtpy import QtWidgets
from UI3.mainwindow import Ui_MainWindow
from newStudent import newStudent

app = QtWidgets.QApplication(sys.argv)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self,parent = None):
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Studierendenverwaltung")

        with open("studenten.csv",newline="", encoding='utf-8') as file:
            csv_file = csv.reader(file,delimiter=',')
            for line in csv_file:
                row = self.ui.tableWidget.rowCount()

                self.ui.tableWidget.insertRow(row)
                self.ui.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(line[0]))
                self.ui.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(line[1]))
                self.ui.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(line[2]))

        self.ui.closeWindow.clicked.connect(self.close_Window_click)
        self.ui.newStudent.clicked.connect(self.new_Student_click)
        self.ui.saveTable.clicked.connect(self.save_Button_click)

    def save_Button_click(self):

        row = self.ui.tableWidget.rowCount()

        with open("studenten.csv",'w',newline="",encoding='utf-8') as file:
            csv_file = csv.writer(file,delimiter=',',quotechar='"')

            for item in range(0,row):
                name = self.ui.tableWidget.item(item,0).text()
                vorname = self.ui.tableWidget.itQQem(item,1).text()
                studiengang = self.ui.tableWidget.item(item,2).text()
                csv_file.writerow([str(name),str(vorname),str(studiengang)])

    def new_Student_click(self):
        row = self.ui.tableWidget.rowCount()
        self.newEntry = newStudent()

    def close_Window_click(self):
        self.close()


window = MainWindow()
window.show()

sys.exit(app.exec_())