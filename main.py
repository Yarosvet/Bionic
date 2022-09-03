from PyQt5.QtWidgets import QApplication
from gui_control import MainWin
from config import Config

if __name__ == "__main__":
    app = QApplication([])
    cf = Config()
    mainwin = MainWin(config=cf)
    mainwin.show()
    app.exec()
