from PyQt5.QtCore import QObject, pyqtSignal


class Rub(QObject):
    mySignal = pyqtSignal(float)


rub = Rub()
