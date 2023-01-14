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
        if self.ui.rb_a.isChecked():
            stage_id = self.current_stage["thesis"]["target_id"]
            if not self.current_stage["thesis"]["is_end"]:
                self.set_base_stage(stage_id)
                self.history_next_stage[stage_id] = 0
            else:
                self.res_window.set_end_stage(self.book_path, stage_id)
                self.res_window.show()
                self.close()
        else:
            stage_id = self.current_stage["antithesis"]["target_id"]
            if not self.current_stage["antithesis"]["is_end"]:
                self.set_base_stage(stage_id)
                self.history_next_stage[stage_id] = 1
            else:
                self.res_window.set_end_stage(self.book_path, stage_id)
                self.res_window.show()
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
            stage = find_stage_by_id(self.stages, self.history_stages[-2])
            if stage["thesis"]["target_id"] == self.history_stages[-1]:
                self.ui.rb_a.setChecked(True)
                self.ui.rb_b.setChecked(False)
            elif stage["antithesis"]["target_id"] == self.history_stages[-1]:
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
            self.ui.caption_a.setText(self.current_stage["thesis"]["caption"])
            self.ui.caption_b.setText(self.current_stage["antithesis"]["caption"])
            self.ui.pic_a.setPixmap(QPixmap(None))
            if self.current_stage["thesis"]["picture"] is not None:
                pic = QPixmap(os.path.join(self.book_path, self.current_stage["thesis"]["picture"]))
                if pic.width() > 500:
                    pic = pic.scaledToWidth(500)
                self.ui.pic_a.setPixmap(pic)
            self.ui.pic_b.setPixmap(QPixmap(None))
            if self.current_stage["antithesis"]["picture"] is not None:
                pic = QPixmap(os.path.join(self.book_path, self.current_stage["antithesis"]["picture"]))
                if pic.width() > 500:
                    pic = pic.scaledToWidth(500)
                self.ui.pic_b.setPixmap(pic)
        except Exception as exc:
            self.error_dialog.showMessage(str(exc))

    def set_base_stage(self, stage_id):
        self.set_stage(stage_id)
        self.history_stages.append(stage_id)
