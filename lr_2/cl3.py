from PyQt5.QtCore import QObject, pyqtSignal


class Euro(QObject):
    mySignal = pyqtSignal(float)


euro = Euro()
