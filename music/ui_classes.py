from utils import set_blur_effect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainterPath, QRegion
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame
from PyQt5.QtCore import QPoint
from PyQt5.uic import loadUi
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, QRectF

# Musiqa
class MusicWindow(QFrame):
    def __init__(self):
        super(MusicWindow, self).__init__()
        loadUi("designs/music.ui", self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.close_btn.clicked.connect(self.close)
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        set_blur_effect(self)

    # move qilish uchun
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        try:
            delta = QPoint(event.globalPos() - self.oldPos)
        except:
            self.oldPos = event.globalPos()
            return
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.oldPos = None

    def paintEvent(self, event):
        # Optional: use this to apply smooth edges (anti-alias)
        path = QPainterPath()
        rect = QRectF(self.rect())
        path.addRoundedRect(rect, 10, 10)

        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)
