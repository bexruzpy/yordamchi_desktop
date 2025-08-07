from components import FullScreenFrame
# from 

class BrowserFrame(FullScreenFrame):
    def __init__(self, *args, **kvargs):
        super(BrowserFrame, self).__init__("browser.ui", *args, **kvargs)

