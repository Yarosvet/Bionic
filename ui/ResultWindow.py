from PyQt5.QtWidgets import QErrorMessage, QWidget
from PyQt5.QtGui import QPixmap
import json
import os

from .tools import find_stage_by_id
from .qt_generated.result import Ui_ResultForm


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
