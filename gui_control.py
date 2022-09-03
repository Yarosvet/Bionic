from PyQt5.QtWidgets import QMainWindow, QDialog, QFileDialog, QErrorMessage, QListWidgetItem, QWidget, QDesktopWidget
from PyQt5.QtGui import QCursor, QPixmap, QCloseEvent, QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QStringListModel, QModelIndex
from ui.main_window import Ui_MainWindow
from ui.add_dialog import Ui_AddDialog
from ui.itembook_widget import Ui_itemWidget
from ui.entry_points import Ui_entryPointsView
from ui.determinant import Ui_Determinant
from ui.result import Ui_ResultForm
from ui.settings import Ui_SettingsForm
import requests
import json
from tarfile import TarFile
import os
from shutil import rmtree


def check_by_filter(text, filter_expression="") -> bool:
    if filter_expression == "":
        return True
    for el in filter_expression.split():
        if el not in text:
            return False
    return True


class MainWin(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.error_dialog = QErrorMessage()
        self.error_dialog.setModal(True)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.determWidget = DetermWidget(self)
        self.entry_tree_widget = EntryPointsView(self, self.determWidget)
        self.entry_tree_widget.set_on_select(self.close)
        self.addDialog = AddDialog(self, self.config, onclose_func=self.update_list_books)
        self.settingsWindow = SettingsForm(self, self.config)
        self.ui.add_button.clicked.connect(self.add_clicked)
        self.ui.listBooks.doubleClicked.connect(self.book_selected)
        self.ui.searchfield.textChanged.connect(self.search_update)
        self.ui.settings_button.clicked.connect(self.settings_clicked)
        self.update_list_books()

    def showEvent(self, a0) -> None:
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def search_update(self):
        image_str = "image: url(:/img/img/search.png) right;"
        stsheet = self.ui.searchfield.styleSheet()
        if self.ui.searchfield.text().strip() != "":
            stsheet = stsheet.replace(image_str, "")
        elif image_str not in stsheet:
            stsheet += image_str
        self.ui.searchfield.setStyleSheet(stsheet)
        self.update_list_books(self.ui.searchfield.text())

    def update_addbook_hint(self):
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
        self.valid_book_paths = []
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
                    item_widget = BookItemWidget(parent=self, cover_path=cover, name=book["name"],
                                                 date=book["translation_date"])
                    item.setSizeHint(item_widget.size())
                    self.ui.listBooks.addItem(item)
                    self.ui.listBooks.setItemWidget(item, item_widget)
                    self.valid_book_paths.append(book_path)
            except Exception as exc:
                self.error_dialog.showMessage(str(exc))
        self.update_addbook_hint()

    def add_clicked(self):
        self.addDialog.show()

    def book_selected(self, index: QModelIndex):
        try:
            self.entry_tree_widget.show()
            self.entry_tree_widget.set_book(self.valid_book_paths[index.row()])
        except Exception as exc:
            self.error_dialog.showMessage(str(exc))

    def settings_clicked(self):
        self.settingsWindow.show()


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


def find_point_by_id(entry_points, p_id: int):
    for el in entry_points:
        if el["id"] == p_id:
            return el
        if el["nested"]:
            res = find_point_by_id(el["nested"], p_id=p_id)
            if res is not None:
                return res
    return None


def find_stage_by_id(stages, s_id: int):
    for el in stages:
        if el["id"] == s_id:
            return el
    return None


class AddDialog(QDialog):
    def __init__(self, parent, config, onclose_func=None):
        super().__init__(parent)
        self.onclose_func = onclose_func
        self.config = config
        self.github_rels = None
        self.error_dialog = QErrorMessage()
        self.error_dialog.setModal(True)
        self.ui = Ui_AddDialog()
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
            a = self.config["rels"]
            req = requests.get(self.config["rels"])
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
    def __init__(self, parent, cover_path: str, name: str, date: str):
        super().__init__(parent)
        self.setupUi(self)
        self.cover_label.setPixmap(QPixmap(cover_path))
        self.name_label.setText(name)
        self.date_label.setText(date)


class EntryPointsView(QWidget):
    def __init__(self, parent, determ_widget):
        super().__init__()
        self.parent_window = parent
        self.on_select_func = None
        self.determ_widget = determ_widget
        self.ui = Ui_entryPointsView()
        self.ui.setupUi(self)
        self.book = None
        self.book_path = None
        self.error_dialog = QErrorMessage()
        self.error_dialog.setModal(True)
        self.treeModel = QStandardItemModel()
        self.treeModel.setHorizontalHeaderLabels(["Entry points"])
        self.ui.treePoints.setModel(self.treeModel)
        self.ui.treePoints.clicked.connect(self.onclick_item)
        self.ui.treePoints.doubleClicked.connect(self.ondbclick_item)

    def showEvent(self, a0) -> None:
        a0.accept()
        self.move(self.parent_window.frameGeometry().center().x() - self.frameGeometry().width() / 2,
                  self.parent_window.frameGeometry().center().y() - self.frameGeometry().height() / 2)

    def set_on_select(self, func=None):
        self.on_select_func = func

    def set_book(self, book_path: str):
        self.book_path = book_path
        try:
            with open(os.path.join(book_path, "book.json"), 'r') as f:
                self.book = json.load(f)
            self.ui.treePoints.rootNode = self.ui.treePoints.model().invisibleRootItem()
            for i in range(self.treeModel.rowCount()):
                self.treeModel.takeRow(i)
            self.build_tree(self.ui.treePoints.model().invisibleRootItem(), self.book["entry_points"])
            self.ui.treePoints.expandAll()
        except Exception as exc:
            self.error_dialog.showMessage(str(exc))

    def build_tree(self, parent: QStandardItem, entry_points):
        if not entry_points:
            return
        for p in entry_points:
            item = QStandardItem(p["name"])
            item.setData(p["id"])
            parent.appendRow([item])
            self.build_tree(item, p["nested"])

    def onclick_item(self):
        point_id = self.treeModel.itemFromIndex(self.ui.treePoints.selectedIndexes()[0]).data()
        try:
            point = find_point_by_id(self.book["entry_points"], point_id)
            self.ui.point_name.setText(point["name"])
            self.ui.pointText.setText(point["caption"])
        except Exception as exc:
            self.error_dialog.showMessage(str(exc))

    def ondbclick_item(self):
        point_id = self.treeModel.itemFromIndex(self.ui.treePoints.selectedIndexes()[0]).data()
        point = find_point_by_id(self.book["entry_points"], point_id)
        try:
            self.close()
            self.determ_widget.clear_history()
            self.determ_widget.open_book(self.book_path)
            self.determ_widget.set_basestage(point["stage_id"])
            self.determ_widget.show()
            if self.on_select_func is not None:
                self.on_select_func()
        except Exception as exc:
            self.error_dialog.showMessage(str(exc))


class DetermWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent_window = parent
        self.ui = Ui_Determinant()
        self.ui.setupUi(self)
        self.res_window = ResultWindow(self, parent)
        self.error_dialog = QErrorMessage()
        self.error_dialog.setModal(True)
        self.book_path = None
        self.stages = None
        self.history_stages = []
        self.history_next_stage = {}
        self.current_stage = None
        self.ui.next_button.clicked.connect(self.go_next)
        self.ui.back_button.clicked.connect(self.go_back)

    def showEvent(self, a0) -> None:
        a0.accept()
        self.move(self.parent_window.frameGeometry().center().x() - self.frameGeometry().width() / 2,
                  self.parent_window.frameGeometry().center().y() - self.frameGeometry().height() / 2)

    def go_next(self):
        if not self.current_stage["is_end"]:
            if self.ui.rb_a.isChecked():
                stage_id = self.current_stage["variants"][0]["target_id"]
                self.set_basestage(stage_id)
                self.history_next_stage[stage_id] = 0
            else:
                stage_id = self.current_stage["variants"][1]["target_id"]
                self.set_basestage(stage_id)
                self.history_next_stage[stage_id] = 1
        else:
            self.close()

    def go_back(self):
        if len(self.history_stages) <= 1:
            return
        if self.ui.rb_a.isChecked():
            self.history_next_stage[self.current_stage["id"]] = 0
        else:
            self.history_next_stage[self.current_stage["id"]] = 1
        self.set_stage(self.history_stages[-2])
        try:
            variants = find_stage_by_id(self.stages, self.history_stages[-2])["variants"]
            if variants[0]["target_id"] == self.history_stages[-1]:
                self.ui.rb_a.setChecked(True)
                self.ui.rb_b.setChecked(False)
            elif variants[1]["target_id"] == self.history_stages[-1]:
                self.ui.rb_a.setChecked(False)
                self.ui.rb_b.setChecked(True)
            self.history_stages.pop(-1)
        except Exception as exc:
            self.error_dialog.showMessage(str(exc))

    def clear_history(self):
        self.history_stages.clear()
        self.history_next_stage.clear()

    def open_book(self, book_path: str):
        self.book_path = book_path
        try:
            with open(os.path.join(book_path, "book.json"), 'r') as fb:
                with open(os.path.join(book_path, json.load(fb)["stages"]), 'r') as fs:
                    self.stages = json.load(fs)
        except Exception as exc:
            self.error_dialog.showMessage(str(exc))

    def set_stage(self, stage_id):
        try:
            ex_stage = find_stage_by_id(self.stages, stage_id)
            if not ex_stage["is_end"]:
                self.current_stage = ex_stage
                self.ui.text_field.setText(self.current_stage["text"])
                self.ui.rb_a.setVisible(True)
                self.ui.rb_b.setVisible(True)
                if stage_id in self.history_next_stage.keys():
                    if self.history_next_stage[stage_id] == 0:
                        self.ui.rb_a.setChecked(True)
                        self.ui.rb_b.setChecked(False)
                    elif self.history_next_stage[stage_id] == 1:
                        self.ui.rb_a.setChecked(False)
                        self.ui.rb_b.setChecked(True)
                self.ui.caption_a.setText(self.current_stage["variants"][0]["caption"])
                self.ui.caption_b.setText(self.current_stage["variants"][1]["caption"])
                self.ui.pic_a.setPixmap(QPixmap(None))
                if self.current_stage["variants"][0]["picture"] is not None:
                    pic = QPixmap(os.path.join(self.book_path, self.current_stage["variants"][0]["picture"]))
                    if pic.width() > 500:
                        pic = pic.scaledToWidth(500)
                    self.ui.pic_a.setPixmap(pic)
                self.ui.pic_b.setPixmap(QPixmap(None))
                if self.current_stage["variants"][1]["picture"] is not None:
                    pic = QPixmap(os.path.join(self.book_path, self.current_stage["variants"][1]["picture"]))
                    if pic.width() > 500:
                        pic = pic.scaledToWidth(500)
                    self.ui.pic_b.setPixmap(pic)
            else:
                self.res_window.set_end_stage(self.book_path, stage_id)
                self.res_window.show()
        except Exception as exc:
            self.error_dialog.showMessage(str(exc))

    def set_basestage(self, stage_id):
        self.set_stage(stage_id)
        self.history_stages.append(stage_id)


class ResultWindow(QWidget):
    def __init__(self, parent, base_window):
        super().__init__()
        self.parent_window = parent
        self.ui = Ui_ResultForm()
        self.ui.setupUi(self)
        self.error_dialog = QErrorMessage()
        self.error_dialog.setModal(True)
        self.ui.back_button.clicked.connect(self.go_back)
        self.go_back_flag = False
        self.base_window = base_window

    def showEvent(self, a0) -> None:
        a0.accept()
        self.move(self.parent_window.frameGeometry().center().x() - self.frameGeometry().width() / 2,
                  self.parent_window.frameGeometry().center().y() - self.frameGeometry().height() / 2)

    def set_end_stage(self, book_path, stage_id):
        try:
            with open(os.path.join(book_path, "book.json"), 'r') as fb:
                with open(os.path.join(book_path, json.load(fb)["stages"]), 'r') as fs:
                    all_stages = json.load(fs)
            stage = find_stage_by_id(all_stages, stage_id)
            self.ui.res_text.setText(stage["text"])
            if stage["result_picture"] is not None:
                pic = QPixmap(os.path.join(book_path, stage["result_picture"])).scaledToWidth(500)
                self.ui.res_picture.setPixmap(pic)
        except Exception as exc:
            self.error_dialog.showMessage(str(exc))

    def go_back(self):
        self.go_back_flag = True
        self.close()
        self.go_back_flag = False

    def closeEvent(self, a0) -> None:
        a0.accept()
        if not self.go_back_flag:
            self.parent_window.close()
            self.base_window.show()


class SettingsForm(QWidget):
    def __init__(self, parent, config):
        super().__init__()
        self.parent_window = parent
        self.config = config
        self.ui = Ui_SettingsForm()
        self.ui.setupUi(self)
        self.ui.save_button.clicked.connect(self.save_clicked)

    def showEvent(self, a0) -> None:
        self.ui.rels_lineedit.setText(self.config["rels"])

    def save_clicked(self):
        self.config["rels"] = self.ui.rels_lineedit.text()
        self.config.save()
