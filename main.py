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
from home.ui_classes import HomeWindow
from browser import BrowserFrame


app = QApplication(sys.argv)
home = HomeWindow(window_title="Home")
home.show()

music = MusicWindow(
    follow_frame=home,
    window_title="Musiqa1",
    active_button=home.music_btn
    )
music2 = MusicWindow(
    follow_frame=home,
    window_title="Musiqa2",
    active_button=home.planes_btn
    )
music3 = MusicWindow(
    follow_frame=home,
    window_title="Musiqa3",
    active_button=home.ideas_btn
    )

browser = BrowserFrame(
    window_title="Browser",
    active_button=music.pushButton_4
)

sys.exit(app.exec_())
