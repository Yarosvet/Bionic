from PyQt5.QtWidgets import QMainWindow, QErrorMessage, QListWidgetItem, QDesktopWidget
from PyQt5.QtCore import QModelIndex
import json
import os

from .qt_generated.main_window import Ui_MainWindow
from .tools import install_book, check_by_filter
from .BookItemWidget import BookItemWidget
from .DeterminantWindow import DetermWidget
from .EntryPointsWindow import EntryPointsView
from .AddDialog import AddDialog
from .SettingsWindow import SettingsForm


class MainWin(QMainWindow):
    def __init__(self, config, theme_changer_func):
        super().__init__()
        self.config = config
        self.theme_changer_func = theme_changer_func
        self.error_dialog = QErrorMessage()
        self.error_dialog.setModal(True)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.determWidget = DetermWidget(self, self.config)
        self.entry_tree_widget = EntryPointsView(self, self.config, self.determWidget)
        self.entry_tree_widget.set_on_select(self.close)
        self.addDialog = AddDialog(self, self.config, onclose_func=self.update_list_books)
        self.settingsWindow = SettingsForm(self, self.config)
        self.ui.add_button.clicked.connect(self.add_clicked)
        self.ui.listBooks.doubleClicked.connect(self.book_selected)
        self.ui.searchfield.textChanged.connect(self.search_update)
        self.ui.settings_button.clicked.connect(self.settings_clicked)
        self.ui.darkmode_button.clicked.connect(self.dark_mode_clicked)
        self.update_list_books()

    def showEvent(self, a0) -> None:
        qt_rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

    def search_update(self):
        image_str = "image: url(:/img/img/search.png) right;"
        st_sheet = self.ui.searchfield.styleSheet()
        if self.ui.searchfield.text().strip() != "":
            st_sheet = st_sheet.replace(image_str, "")
        elif image_str not in st_sheet:
            st_sheet += image_str
        self.ui.searchfield.setStyleSheet(st_sheet)
        self.update_list_books(self.ui.searchfield.text())

    def update_add_book_hint(self):
        if self.ui.listBooks.count() == 0:
            self.ui.addbook_label.setFixedHeight(19)
        else:
            self.ui.addbook_label.setFixedHeight(0)

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

    def update_list_books(self, filter_expression=""):
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
                    if not check_by_filter(book["name"], filter_expression=filter_expression):
                        continue
                    cover = ":/img/img/book.png"
                    if book["cover"] is not None:
                        cover = os.path.join(book_path, book["cover"])
                    item = QListWidgetItem(self.ui.listBooks)
                    item_widget = BookItemWidget(parent=self, config=self.config, cover_path=cover, name=book["name"],
                                                 date=book["translation_date"], book_path=book_path)
                    item.setSizeHint(item_widget.size())
                    self.ui.listBooks.addItem(item)
                    self.ui.listBooks.setItemWidget(item, item_widget)
            except Exception as exc:
                self.error_dialog.showMessage(str(exc))
        self.update_add_book_hint()

    def add_clicked(self):
        self.addDialog.show()

    def book_selected(self, index: QModelIndex):
        try:
            self.entry_tree_widget.show()
            book_path = self.ui.listBooks.itemWidget(self.ui.listBooks.item(index.row())).book_path
            self.entry_tree_widget.open_book(book_path=book_path)
        except Exception as exc:
            self.error_dialog.showMessage(str(exc))

    def settings_clicked(self):
        self.settingsWindow.show()

    def dark_mode_clicked(self):
        self.theme_changer_func()
