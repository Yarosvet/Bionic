from .MainWindow import MainWin
from ..config import Config

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase


class BionicUi:
    def __init__(self, app: QApplication):
        self.app = app
        self.app.setStyle('Fusion')
        QFontDatabase.addApplicationFont(":/fonts/fonts/DejaVuSans.ttf")
        self.config = Config()
        self.mw = MainWin(config=self.config)

    def show(self):
        self.mw.show()
