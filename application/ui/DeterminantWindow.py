from PyQt5.QtWidgets import QErrorMessage, QWidget
from .qt_generated.determinant import Ui_Determinant
from .qt_generated.dark.dark_determinant import Ui_DarkDeterminant
from .ResultWindow import ResultWindow
from ..book import Stage, StagesStack


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
        self.stages_stack = StagesStack()
        self.ui.next_button.clicked.connect(self.go_next)
        self.ui.back_button.clicked.connect(self.go_back)

    def showEvent(self, a0) -> None:
        a0.accept()
        self.move(int(self.parent_window.frameGeometry().center().x() - self.frameGeometry().width() / 2),
                  int(self.parent_window.frameGeometry().center().y() - self.frameGeometry().height() / 2))

    def go_next(self):
        self.stages_stack.set_current_thesis(self.ui.rb_a.isChecked())
        if self.ui.rb_a.isChecked():
            stage = self.stages_stack.current_stage().thesis.target
        else:
            stage = self.stages_stack.current_stage().antithesis.target
        if isinstance(stage, Stage):  # Stage
            self.stages_stack.add_stage(stage)
            self.display_current_stage()
        else:  # Ending
            self.res_window.set_end_stage(stage)
            self.res_window.show()
            self.close()

    def go_back(self):
        if not self.stages_stack.can_move_back():
            return
        try:
            self.stages_stack.move_back()
            self.display_current_stage()
        except Exception as exc:
            self.error_dialog.showMessage(str(exc))

    def open_book_on_stage(self, stage: Stage):
        self.stages_stack = StagesStack()
        try:
            self.stages_stack.add_stage(stage)
            self.display_current_stage()
        except Exception as exc:
            self.error_dialog.showMessage(str(exc))

    def set_stage(self, stage: Stage):
        try:
            self.stages_stack.add_stage(stage)
            self.display_current_stage()
        except Exception as exc:
            self.error_dialog.showMessage(str(exc))

    def display_current_stage(self):
        self.ui.rb_a.setChecked(self.stages_stack.thesis_selected())
        self.ui.caption_a.setText(self.stages_stack.current_stage().thesis.document)
        self.ui.caption_b.setText(self.stages_stack.current_stage().antithesis.document)
