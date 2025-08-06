from utils import set_blur_effect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainterPath, QRegion
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame
from PyQt5.QtCore import QPoint
from PyQt5.uic import loadUi
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, QRectF, QEasingCurve, QPropertyAnimation, pyqtSignal
from PyQt5.QtGui import QPainter

# Musiqa
class BaseFrame(QFrame):
    def __init__(self, path, follow_frame=None, active_button=None, follow_distance=10, *args, **kwargs):
        super(BaseFrame, self).__init__()
        loadUi("designs/"+path, self)
        self.move_y = 0

        self.setWindowTitle(kwargs["window_title"])

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.close_btn.clicked.connect(self.close)

        self.active_button = active_button
        if active_button:
            self.active_button.clicked.connect(self.show_func_for_button)

        self.follow_origin = "left"
        self.follow_distance = follow_distance
        self.follow_frame = follow_frame
        self.start_y = 0
        self.follower_frames = []
        if self.follow_frame != None:
            for frame in self.follow_frame.follower_frames:
                self.move_y += frame.height() + self.follow_distance
            self.follow_frame.follower_frames.append(self)
            self.moveEventFollowFrame()
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        set_blur_effect(self)
    def show_func_for_button(self):
        if self.isVisible():
            self.active_button.setStyleSheet("")
            self.close()
            return
        self.active_button.setStyleSheet("""
            QPushButton{
            border: 1px solid;
            border-color: rgba(255, 255, 255, 100);
            background-color: rgba(255, 255, 255, 30);
            padding: 20px;
            font: 25 20px "Segoe UI Black";
            }""")
        self.show()
    def showEvent(self, event):
        if self.follow_frame == None:
            return
        self.follow_frame.start_y = 0

        self.follow_frame.follower_frames.remove(self)
        self.follow_frame.follower_frames.append(self)
        move_y = 0
        for frame in self.follow_frame.follower_frames:
            if frame == self:
                self.move_y = move_y
                move_y += self.height() + self.follow_distance
            elif frame.isVisible():
                frame.move_y = move_y
                move_y += frame.height() + frame.follow_distance
        self.follow_frame.moveEvent("refresh")
    # move qilish uchun
    def mousePressEvent(self, event):
        if self.follow_frame == None:
            self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.follow_frame == None:
            try:
                delta = QPoint(event.globalPos() - self.oldPos)
            except:
                self.oldPos = event.globalPos()
                return
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
    def moveWithAnimation(self, x, y):
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(100)  # 1000 ms = 1 sekund
        self.animation.setStartValue(QPoint(self.x(), self.y()))  # Boshlanish joyi
        self.animation.setEndValue(QPoint(x, y+self.move_y+self.follow_frame.start_y))    # Tugash joyi
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.start()

    def moveEventFollowFrame(self):
        # get follow origin
        self.follow_origin = self.follow_frame.follow_origin
        if self.follow_origin == "right":
            if self.follow_frame.x() + self.follow_frame.width() + self.width() + self.follow_distance > QApplication.desktop().width():
                self.follow_frame.follow_origin = "left"
                return
            # animatsiya orqali move qilish
            self.moveWithAnimation(
                self.follow_frame.x() + self.follow_frame.width() + self.follow_distance,
                self.follow_frame.y()
            )
        elif self.follow_origin == "left":
            if self.follow_frame.x() - self.width() - self.follow_distance < 0:
                self.follow_frame.follow_origin = "right"
                return
            self.moveWithAnimation(
                self.follow_frame.x() - self.width() - self.follow_distance,
                self.follow_frame.y(),
            )
    def moveEvent(self, event):
        for frame in self.follower_frames:
            frame.moveEventFollowFrame()
        
    def mouseReleaseEvent(self, event):
        if self.follow_frame == None:
            self.oldPos = None


    # Close event
    def closeEvent(self, event):
        if self.active_button:
            self.active_button.setStyleSheet("")
        for frame in self.follower_frames:
            frame.close()
        if self.follow_frame != None:
            move_y = 0
            print(len(self.follow_frame.follower_frames))
            for frame in self.follow_frame.follower_frames:
                print(frame != self)
                if frame.isVisible() and frame != self:
                    frame.move_y = move_y
                    move_y += frame.height() + self.follow_distance
            self.follow_frame.moveEvent("refresh follower frames")
    def wheelEvent(self, event):
        delta = event.angleDelta().y()  # faqat vertikal scrollni olayapmiz

        # Harakat miqdori (ixtiyoriy: har 120 da 20 piksel)
        step = 20 if delta > 0 else -20

        # Tepa-pastga harakatlantiramiz
        current_pos = self.pos()
        if self.follow_frame != None:
            self.follow_frame.start_y += step
            self.follow_frame.start_y = min(0, self.follow_frame.start_y)
            self.follow_frame.moveEvent("refresh follower frames")