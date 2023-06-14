from .MainWindow import MainWin
from ..config import Config

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtCore import QFile, QTextStream


class BionicUi:
    def __init__(self, app: QApplication):
        self.app = app
        self.app.setStyle('Fusion')
        QFontDatabase.addApplicationFont(":/fonts/fonts/DejaVuSans.ttf")
        self.config = Config()
        self.init_theme()
        self.mw = MainWin(config=self.config, theme_changer_func=self.change_theme)

    def change_theme(self):
        self.config["dark_mode"] = "1" if not int(self.config["dark_mode"]) else "0"
        self.config.save()
        self.init_theme()

    def init_theme(self):
        file = QFile(":/styles/ui/dark.qss" if int(self.config["dark_mode"]) else ":/styles/ui/light.qss")
        file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(file)
        self.app.setStyleSheet(stream.readAll())

    def show(self):
        self.mw.show()
