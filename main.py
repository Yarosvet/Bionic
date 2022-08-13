from PyQt5.QtWidgets import QApplication
from gui_control import MainWin

if __name__ == "__main__":
    app = QApplication([])
    mainwin = MainWin()
    mainwin.show()
    app.exec()
