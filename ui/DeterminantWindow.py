from PyQt5.QtWidgets import QErrorMessage, QWidget
from PyQt5.QtGui import QPixmap
import json
import os

from .tools import find_stage_by_id
from .qt_generated.determinant import Ui_Determinant
from .qt_generated.dark.dark_determinant import Ui_DarkDeterminant
from .ResultWindow import ResultWindow


class DetermWidget(QWidget):
    def __init__(self, parent, config):
        super().__init__()
        self.parent_window = parent
        self.config = config
        self.ui = Ui_Determinant() if not int(self.config["dark_mode"]) else Ui_DarkDeterminant()
        self.ui.setupUi(self)
        self.res_window = ResultWindow(self, self.config, self.parent_window)
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
                self.set_base_stage(stage_id)
                self.history_next_stage[stage_id] = 0
            else:
                stage_id = self.current_stage["variants"][1]["target_id"]
                self.set_base_stage(stage_id)
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

    def set_base_stage(self, stage_id):
        self.set_stage(stage_id)
        self.history_stages.append(stage_id)
