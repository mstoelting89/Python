import csv
from qtpy import QtWidgets
from UI3.mainwindow import Ui_MainWindow
from NewEntry.mainwindow import Ui_saveWindow
from main import MainWindow


class newStudent(QtWidgets.QMainWindow):
    def __init__(self,parent = None):
        super().__init__(parent)
        self.ui2 = Ui_saveWindow()
        self.ui2.setupUi(self)
        self.show()

        self.ui2.cancelButton.clicked.connect(self.cancel_Button_click)
        self.ui2.saveButton.clicked.connect(self.save_Student_click)

    def cancel_Button_click(self):
        self.close()

    def save_Student_click(self):
        vorname = self.ui2.Vorname.text()
        nachname = self.ui2.Nachname.text()
        studiengang = self.ui2.Studiengang.text()


        #with open("studenten.csv",'a',newline="",encoding='utf-8') as file:
        #    csv_file = csv.writer(file,delimiter=',',quotechar='"')
        #    csv_file.writerow([nachname,vorname,studiengang])


        self.close()
