from PyQt5.QtWidgets import QErrorMessage, QWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import json
import os

from .tools import find_point_by_id
from .qt_generated.entry_points import Ui_entryPointsView


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
        self.ui.treePoints.doubleClicked.connect(self.on_db_click_item)

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

    def on_db_click_item(self):
        point_id = self.treeModel.itemFromIndex(self.ui.treePoints.selectedIndexes()[0]).data()
        point = find_point_by_id(self.book["entry_points"], point_id)
        try:
            self.close()
            self.determ_widget.clear_history()
            self.determ_widget.open_book(self.book_path)
            self.determ_widget.set_base_stage(point["stage_id"])
            self.determ_widget.show()
            if self.on_select_func is not None:
                self.on_select_func()
        except Exception as exc:
            self.error_dialog.showMessage(str(exc))
