import sys
from qtpy import QtWidgets

from UI.mainwindow import Ui_MainWindow

app = QtWidgets.QApplication(sys.argv)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)

        self.setWindowTitle("Tabellen darstellen")

        self.ui.tableWidget.cellChanged.connect(self.on_CellChanged)
        self.ui.pushButton.clicked.connect(self.on_pushButton_click)

    def on_CellChanged(self, row, col):
        print(row)
        print(col)

    def on_pushButton_click(self):

        row = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.insertRow(row)

        self.ui.tableWidget.setItem(row,0, QtWidgets.QTableWidgetItem("Budapest"))
        self.ui.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem("12345"))

        print("Button wurde geklickt")


window = MainWindow()
window.show()

sys.exit(app.exec_())

