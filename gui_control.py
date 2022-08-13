from PyQt5.QtWidgets import QMainWindow
from main_window import Ui_MainWindow


class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
