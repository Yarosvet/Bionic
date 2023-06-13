from PyQt5.QtWidgets import QErrorMessage, QWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import os

from .qt_generated.entry_points import Ui_entryPointsView
from .qt_generated.dark.dark_entry_points import Ui_DarkEntryPointsView
from ..book import Book


class EntryPointsView(QWidget):
    def __init__(self, parent, config, determ_widget):
        super().__init__()
        self.parent_window = parent
        self.config = config
        self.on_select_func = None
        self.determ_widget = determ_widget
        self.ui = Ui_entryPointsView() if not int(self.config["dark_mode"]) else Ui_DarkEntryPointsView()
        self.ui.setupUi(self)
        self.book = None
        self.error_dialog = QErrorMessage()
        self.error_dialog.setModal(True)
        self.treeModel = QStandardItemModel()
        self.treeModel.setHorizontalHeaderLabels(["Entry points"])
        self.ui.treePoints.setModel(self.treeModel)
        self.ui.treePoints.clicked.connect(self.onclick_item)
        self.ui.treePoints.doubleClicked.connect(self.on_db_click_item)

    def showEvent(self, a0) -> None:
        a0.accept()
        self.move(int(self.parent_window.frameGeometry().center().x() - self.frameGeometry().width() / 2),
                  int(self.parent_window.frameGeometry().center().y() - self.frameGeometry().height() / 2))

    def set_on_select(self, func=None):
        self.on_select_func = func

    def open_book(self, book_path: str):
        try:
            self.book = Book(book_path)
            self.ui.treePoints.rootNode = self.ui.treePoints.model().invisibleRootItem()
            for i in range(self.treeModel.rowCount()):
                self.treeModel.takeRow(i)
            self.build_tree(self.ui.treePoints.model().invisibleRootItem(), self.book.entry_points)
            self.ui.treePoints.expandAll()
        except Exception as exc:
            self.error_dialog.showMessage(str(exc))

    def build_tree(self, parent: QStandardItem, entry_points):
        if not entry_points:
            return
        for p in entry_points:
            item = QStandardItem(p.name)
            item.setData(p.id)
            parent.appendRow([item])
            self.build_tree(item, p.nested)

    def onclick_item(self):
        point_id = self.treeModel.itemFromIndex(self.ui.treePoints.selectedIndexes()[0]).data()
        try:
            point = self.book.get_entry_point(point_id)
            self.ui.point_name.setText(point.name)
            self.ui.pointText.setText(point.caption)
        except Exception as exc:
            self.error_dialog.showMessage(str(exc))

    def on_db_click_item(self):
        point_id = self.treeModel.itemFromIndex(self.ui.treePoints.selectedIndexes()[0]).data()
        point = self.book.get_entry_point(point_id)
        try:
            self.close()
            self.determ_widget.open_book_on_stage(point.stage())
            self.determ_widget.show()
            if self.on_select_func is not None:
                self.on_select_func()
        except Exception as exc:
            self.error_dialog.showMessage(str(exc))
