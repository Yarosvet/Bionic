from PyQt5.QtWidgets import QDialog, QFileDialog, QErrorMessage
from PyQt5.QtGui import QCursor, QCloseEvent
from PyQt5.QtCore import Qt, QStringListModel, QModelIndex
import requests
import json
import os

from .tools import install_book
from .qt_generated.add_dialog import Ui_AddDialog
from .qt_generated.dark.dark_add_dialog import Ui_DarkAddDialog


class AddDialog(QDialog):
    def __init__(self, parent, config, onclose_func=None):
        super().__init__(parent)
        self.onclose_func = onclose_func
        self.config = config
        self.web_rels = None
        self.error_dialog = QErrorMessage()
        self.error_dialog.setModal(True)
        self.ui = Ui_AddDialog() if not int(self.config["dark_mode"]) else Ui_DarkAddDialog()
        self.ui.setupUi(self)
        self.ui.select_button.clicked.connect(self.select_clicked)
        self.ui.get_button.clicked.connect(self.get_clicked)
        self.ui.listbooks.doubleClicked.connect(self.book_clicked)

    def showEvent(self, a0) -> None:
        a0.accept()
        self.move(self.parent().frameGeometry().center().x() - self.frameGeometry().width() / 2,
                  self.parent().frameGeometry().center().y() - self.frameGeometry().height() / 2)

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
            req = requests.get(self.config["rels"])
            if req.status_code == 200:
                self.web_rels = json.loads(req.content)
                self.web_rels["books"] = sorted(self.web_rels["books"], key=lambda x: x["id"])
                model = QStringListModel([book["name"] for book in self.web_rels["books"]])
                self.ui.listbooks.setModel(model)
            else:
                self.error_dialog.showMessage(f"Request code: {req.status_code}")
        except Exception as exc:
            self.error_dialog.showMessage(str(exc))
        self.ui.listbooks.setCursor(QCursor(Qt.ArrowCursor))

    def book_clicked(self, index_m: QModelIndex):
        book = self.web_rels["books"][index_m.row()]
        req = requests.get(self.web_rels["link_prefix"] + book["path"])
        if req.status_code == 200:
            with open("book_{}.tar.gz".format(book["id"]), 'wb') as f:
                f.write(req.content)
            try:
                install_book("book_{}.tar.gz".format(book["id"]), book["id"])
                os.remove("book_{}.tar.gz".format(book["id"]))
                self.close()
            except Exception as exc:
                self.error_dialog.showMessage(str(exc))
