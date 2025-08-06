from components import BaseFrame
class HomeWindow(BaseFrame):
    def __init__(self, *args, **kwargs):
        super(HomeWindow, self).__init__("home.ui", *args, **kwargs)

