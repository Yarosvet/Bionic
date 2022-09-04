from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap

from .qt_generated.itembook_widget import Ui_itemWidget


class BookItemWidget(QWidget, Ui_itemWidget):
    def __init__(self, parent, cover_path: str, name: str, date: str, book_path: str):
        super().__init__(parent)
        self.book_path = book_path
        self.setupUi(self)
        self.cover_label.setPixmap(QPixmap(cover_path))
        self.name_label.setText(name)
        self.date_label.setText(date)
