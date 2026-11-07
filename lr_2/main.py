from PyQt5.QtWidgets import *
import sys

import cl1
import cl2
import cl3


class Data:
    def __init__(self):
        self.myData = {"Рубли": 90.0, "Доллары": 1.0, "Евро": 0.92}

    def getData(self):
        return self.myData


class Some(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лабораторная 2 - рубль / доллар / евро")
        self.rates = Data().getData()

        self.edits = {"Рубли": QLineEdit(), "Доллары": QLineEdit(), "Евро": QLineEdit()}
        self.signals = {
            "Рубли": cl1.rub.mySignal,
            "Доллары": cl2.dollar.mySignal,
            "Евро": cl3.euro.mySignal,
        }

        form = QFormLayout()
        for name, edit in self.edits.items():
            form.addRow(name, edit)
        central = QWidget()
        central.setLayout(form)
        self.setCentralWidget(central)

        for name, edit in self.edits.items():
            edit.textEdited.connect(lambda text, n=name: self.onEdited(n, text))
            self.signals[name].connect(lambda value, n=name: self.updateOthers(n, value))

    def onEdited(self, name, text):
        try:
            self.signals[name].emit(float(text.replace(",", ".")))
        except ValueError:
            for other, edit in self.edits.items():
                if other != name:
                    edit.clear()

    def updateOthers(self, name, value):
        dollars = value / self.rates[name]
        for other, edit in self.edits.items():
            if other != name:
                edit.setText(f"{dollars * self.rates[other]:.2f}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Some()
    window.show()
    app.exec()
