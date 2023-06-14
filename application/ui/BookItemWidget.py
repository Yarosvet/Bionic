from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap

from .qt_generated.itembook_widget import Ui_itemWidget


class BookItemWidget(QWidget):
    def __init__(self, parent, config, cover_path: str, name: str, date: str, book_path: str):
        super().__init__(parent)
        self.book_path = book_path
        self.config = config
        self.ui = Ui_itemWidget()
        self.ui.setupUi(self)
        self.ui.cover_label.setPixmap(QPixmap(cover_path))
        self.ui.name_label.setText(name)
        self.ui.date_label.setText(date)
