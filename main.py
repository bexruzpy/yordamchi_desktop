import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QFrame,
    QVBoxLayout,
    QLabel,
    QGraphicsBlurEffect
)
from PyQt5.QtGui import QRegion, QPainterPath
from PyQt5.QtGui import QPixmap
from music.ui_classes import MusicWindow



app = QApplication(sys.argv)

music = MusicWindow()
music.show()

sys.exit(app.exec_())
