from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase
from ui.MainWindow import MainWin
from config import Config

if __name__ == "__main__":
    app = QApplication([])
    QFontDatabase.addApplicationFont(":/fonts/fonts/DejaVuSans.ttf") 
    cf = Config()
    main_window = MainWin(config=cf)
    main_window.show()
    app.exec()
