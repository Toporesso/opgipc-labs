import sys
import numpy as np
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap, QPainter
from PyQt5.QtCore import Qt


def make_image():
    img = np.full((250, 300, 3), (255, 230, 200), dtype=np.uint8)
    cv2.rectangle(img, (0, 200), (300, 250), (80, 170, 60), -1)
    cv2.rectangle(img, (80, 110), (220, 210), (130, 190, 240), -1)
    cv2.fillPoly(img, [np.array([(65, 115), (150, 50), (235, 115)], dtype=np.int32)], (40, 40, 160))
    cv2.rectangle(img, (135, 150), (170, 210), (40, 80, 130), -1)
    cv2.rectangle(img, (95, 130), (125, 160), (255, 220, 120), -1)
    cv2.rectangle(img, (175, 130), (205, 160), (255, 220, 120), -1)
    cv2.circle(img, (260, 40), 22, (0, 220, 255), -1)
    return cv2.resize(img, (120, 100))


def make_shape(w, h):
    img = np.zeros((h, w, 4), dtype=np.uint8)
    triangle = np.array([(w // 2, 0), (0, h - 1), (w - 1, h - 1)], dtype=np.int32)
    cv2.fillPoly(img, [triangle], (200, 150, 50, 160))
    cv2.polylines(img, [triangle], True, (0, 0, 0, 255), 3)
    return img


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лабораторная 1")
        self.resize(400, 300)
        self.shape_pixmap = None

        self.label = QLabel("Надпись")
        self.label.setAlignment(Qt.AlignCenter)
        self.button1 = QPushButton("Кнопка 1")
        self.button2 = QPushButton("Кнопка 2")
        self.button1.clicked.connect(self.on_button1)
        self.button2.clicked.connect(self.on_button2)

        buttons = QHBoxLayout()
        buttons.addWidget(self.button1)
        buttons.addWidget(self.button2)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.label)
        self.main_layout.addLayout(buttons)
        self.normal_margins = self.main_layout.contentsMargins()

    def on_button1(self):
        if self.label.pixmap() is None or self.label.pixmap().isNull():
            img = make_image()
            h, w, _ = img.shape
            qimg = QImage(img.data, w, h, 3 * w, QImage.Format_RGB888).rgbSwapped()
            self.label.setPixmap(QPixmap.fromImage(qimg))
        else:
            self.label.setPixmap(QPixmap())
            self.label.setText("Надпись")

    def on_button2(self):
        geo = self.geometry()
        if self.shape_pixmap is None:
            w, h = geo.width(), geo.height()
            img = make_shape(w, h)
            qimg = QImage(img.data, w, h, 4 * w, QImage.Format_ARGB32)
            self.shape_pixmap = QPixmap.fromImage(qimg)

            self.main_layout.setContentsMargins(int(0.15 * w), int(0.3 * h), int(0.15 * w), int(0.1 * h))
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.setGeometry(geo)
            self.setMask(self.shape_pixmap.mask())
            self.setWindowOpacity(0.8)
        else:
            self.shape_pixmap = None
            self.main_layout.setContentsMargins(self.normal_margins)
            self.clearMask()
            self.setWindowOpacity(1.0)
            self.setWindowFlags(Qt.Window)
            self.setGeometry(geo)
        self.show()

    def paintEvent(self, event):
        if self.shape_pixmap is not None:
            QPainter(self).drawPixmap(self.rect(), self.shape_pixmap)


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())
