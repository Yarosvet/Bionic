from PyQt5.QtWidgets import QApplication

from .ui import BionicUi


class BionicApplication:
    def __init__(self):
        self.qt_app = QApplication([])
        self.b_ui = BionicUi(self.qt_app)
        self.b_ui.show()
        self.qt_app.exec()
