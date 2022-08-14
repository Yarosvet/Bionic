from PyQt5.QtWidgets import QMainWindow, QDialog, QFileDialog, QErrorMessage, QListWidgetItem, QWidget
from PyQt5.QtGui import QCursor, QPixmap, QCloseEvent, QDropEvent
from PyQt5.QtCore import Qt, QStringListModel, QModelIndex, QEvent
from main_window import Ui_MainWindow
from add_dialog import Ui_AddDialog
from itembook_widget import Ui_itemWidget
import requests
import json
from tarfile import TarFile
import os
from shutil import rmtree


class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.error_dialog = QErrorMessage()
        self.error_dialog.setModal(True)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.addDialog = AddDialog(self.update_list_books)
        self.ui.add_button.clicked.connect(self.add_clicked)
        self.update_list_books()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                try:
                    install_book(url.path())
                    self.update_list_books()
                except Exception as exc:
                    self.error_dialog.showMessage(str(exc))
            event.acceptProposedAction()

    def update_list_books(self):
        for i in range(self.ui.listBooks.count()):
            self.ui.listBooks.takeItem(i)
        if not os.path.exists("books/"):
            return
        for el in os.listdir("books/"):
            book_path = os.path.join("books/", el)
            try:
                if os.path.isdir(book_path) and os.path.exists(os.path.join(book_path, "book.json")):
                    with open(os.path.join(book_path, "book.json"), 'r') as f:
                        book = json.load(f)
                    cover = ":/img/img/book.png"
                    if book["cover"] is not None:
                        cover = os.path.join(book_path, book["cover"])
                    item = QListWidgetItem(self.ui.listBooks)
                    item_widget = BookItemWidget(cover_path=cover, name=book["name"], date=book["translation_date"])
                    item.setSizeHint(item_widget.size())
                    self.ui.listBooks.addItem(item)
                    self.ui.listBooks.setItemWidget(item, item_widget)
            except Exception as exc:
                self.error_dialog.showMessage(str(exc))

    def add_clicked(self):
        self.addDialog.show()


def install_book(tar_path, book_id=None):
    if not os.path.exists("books/"):
        os.mkdir("books/")
    if book_id is None:
        with TarFile.open(name=tar_path, mode="r") as tf:
            tf.extract("book.json", "temp/")
        with open("temp/book.json", 'r') as f:
            book_id = json.load(f)["id"]
        os.remove("temp/book.json")
    book_path = f"books/book_{book_id}/"
    if os.path.exists(book_path):
        rmtree(book_path)
    os.mkdir(book_path)
    with TarFile.open(name=tar_path, mode="r") as tf:
        tf.extractall(path=book_path)


class AddDialog(QDialog):
    def __init__(self, onclose_func=None):
        super().__init__()
        self.onclose_func = onclose_func
        self.github_rels = None
        self.error_dialog = QErrorMessage()
        self.error_dialog.setModal(True)
        self.ui = Ui_AddDialog()
        self.ui.setupUi(self)
        self.ui.select_button.clicked.connect(self.select_clicked)
        self.ui.get_button.clicked.connect(self.get_clicked)
        self.ui.listbooks.doubleClicked.connect(self.book_clicked)

    def closeEvent(self, a0: QCloseEvent) -> None:
        if self.onclose_func:
            self.onclose_func()

    def select_clicked(self):
        files = QFileDialog.getOpenFileNames(parent=self, caption="Select one or more book-files *.tar.gz",
                                             filter="Archive GZIP (*.tar.gz);;All files (*.*)")[0]
        try:
            for el in files:
                install_book(el)
            self.close()
        except Exception as exc:
            self.error_dialog.showMessage(str(exc))

    def get_clicked(self):
        self.ui.listbooks.setCursor(QCursor(Qt.WaitCursor))
        try:
            req = requests.get("https://raw.githubusercontent.com/Yarosvet/Bionic_books/master/rels.json")
            if req.status_code == 200:
                self.github_rels = json.loads(req.content)
                self.github_rels["books"] = sorted(self.github_rels["books"], key=lambda x: x["id"])
                model = QStringListModel([book["name"] for book in self.github_rels["books"]])
                self.ui.listbooks.setModel(model)
            else:
                self.error_dialog.showMessage(f"Request code: {req.status_code}")
        except Exception as exc:
            self.error_dialog.showMessage(str(exc))
        self.ui.listbooks.setCursor(QCursor(Qt.ArrowCursor))

    def book_clicked(self, index_m: QModelIndex):
        book = self.github_rels["books"][index_m.row()]
        req = requests.get(self.github_rels["link_prefix"] + book["path"])
        if req.status_code == 200:
            with open("book_{}.tar.gz".format(book["id"]), 'wb') as f:
                f.write(req.content)
            try:
                install_book("book_{}.tar.gz".format(book["id"]), book["id"])
                os.remove("book_{}.tar.gz".format(book["id"]))
                self.close()
            except Exception as exc:
                self.error_dialog.showMessage(str(exc))


class BookItemWidget(QWidget, Ui_itemWidget):
    def __init__(self, cover_path: str, name: str, date: str):
        super().__init__()
        self.setupUi(self)
        self.cover_label.setPixmap(QPixmap(cover_path))
        self.name_label.setText(name)
        self.date_label.setText(date)
