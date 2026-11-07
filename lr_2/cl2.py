from PyQt5.QtCore import QObject, pyqtSignal


class Dollar(QObject):
    mySignal = pyqtSignal(float)


dollar = Dollar()
