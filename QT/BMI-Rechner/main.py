import sys
from qtpy import QtWidgets
from UI.mainwindow import Ui_MainWindow

app = QtWidgets.QApplication(sys.argv)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("BMI-Rechner")
        self.ui.calculate.clicked.connect(self.calculate)

    def calculate(self):
        self.ui.result.setText("")

        weight = self.ui.weight.value()
        height = self.ui.height.value()

        # sneak_case => wird in Python verwendet
        # camelCase
        # PascalCase

        if weight <= 0 or height <= 0:
            self.ui.result.setText("Bitte gebe eine korrekte Zahl ein")
        else:
            result = round((weight / (height ** 2)),2)
            self.ui.result.setText(str(result))

window = MainWindow()

window.show()

sys.exit(app.exec_())


