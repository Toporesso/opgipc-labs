import sys
import os
from PyQt5.QtCore import QUrl, QObject, QTimer, QMetaObject, Qt, Q_ARG, Q_RETURN_ARG
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtQuick import QQuickWindow


SAVE_INTERVAL_MS = 5000
SAVE_FILE = "canvas.png"


class Interface(QObject):
    def __init__(self):
        super().__init__()
        self.canvas = None
        self.path = os.path.abspath(SAVE_FILE)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.save_canvas)

    def start(self, window):
        self.canvas = self.find_canvas(window.contentItem())
        if self.canvas is None:
            print("Ошибка: Canvas в QML не найден!")
            return
        self.timer.start(SAVE_INTERVAL_MS)

    def find_canvas(self, item):
        if item.inherits("QQuickCanvasItem"):
            return item
        for child in item.childItems():
            found = self.find_canvas(child)
            if found is not None:
                return found
        return None

    def save_canvas(self):
        ok = QMetaObject.invokeMethod(self.canvas, "save", Qt.DirectConnection,
                                      Q_RETURN_ARG(bool), Q_ARG(str, self.path))
        if ok:
            print("Canvas сохранён:", self.path)
        else:
            print("Не удалось сохранить canvas")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    interface = Interface()
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("_backend", interface)

    engine.load("mainWindow.qml")

    if not engine.rootObjects():
        print("Ошибка: Не удалось загрузить QML файл!")
        sys.exit(-1)

    interface.start(engine.rootObjects()[0])

    sys.exit(app.exec())
