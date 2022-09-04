from PyQt5.QtWidgets import QApplication
from ui.MainWindow import MainWin
from config import Config

if __name__ == "__main__":
    app = QApplication([])
    cf = Config()
    main_window = MainWin(config=cf)
    main_window.show()
    app.exec()
