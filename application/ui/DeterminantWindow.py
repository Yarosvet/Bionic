from PyQt5.QtWidgets import QErrorMessage, QWidget
import lxml.html
import traceback
import base64
from PIL import Image
import io

from .qt_generated.determinant import Ui_Determinant
from .ResultWindow import ResultWindow
from ..book import Stage, StagesStack


class DetermWidget(QWidget):
    def __init__(self, parent, config):
        super().__init__()
        self.parent_window = parent
        self.config = config
        self.flag_on_ending = False
        self.ui = Ui_Determinant()
        self.ui.setupUi(self)
        self.res_window = ResultWindow(self, self.config, self.parent_window)
        self.error_dialog = QErrorMessage()
        self.error_dialog.setModal(True)
        self.stages_stack = StagesStack()
        self.ui.next_button.clicked.connect(self.go_next)
        self.ui.back_button.clicked.connect(self.go_back)
        self.ui.caption_a.resizeEvent = self.on_text_resize_event(self.ui.caption_a.resizeEvent)
        self.ui.caption_b.resizeEvent = self.on_text_resize_event(self.ui.caption_b.resizeEvent)

    def showEvent(self, a0) -> None:
        a0.accept()
        self.move(int(self.parent_window.frameGeometry().center().x() - self.frameGeometry().width() / 2),
                  int(self.parent_window.frameGeometry().center().y() - self.frameGeometry().height() / 2))

    def closeEvent(self, a0) -> None:
        a0.accept()
        if not self.flag_on_ending:
            self.parent_window.show()

    def eventFilter(self, obj, event) -> bool:
        print(2)
        if obj is self.ui.caption_a or obj is self.ui.caption_b:
            print(1)
        return super().eventFilter(obj, event)

    def on_text_resize_event(self, func):
        def do_contents(*args, **kwargs):
            res = func(*args, **kwargs)
            self.resize_images()
            return res

        return do_contents

    def resize_images(self):

        def resize_images_from_doc(doc: str, browser_width: int):
            doc = lxml.html.fromstring(doc)
            for img in doc.xpath("//img"):
                img.attrib['height'] = ''
                uri = img.attrib['src'].split(',')[1]
                with io.BytesIO(base64.b64decode(uri)) as f:
                    orig_width = Image.open(f).width
                img.attrib['width'] = str(min(browser_width, orig_width))
            return lxml.html.tostring(doc).decode('ascii')

        try:
            doc_a = resize_images_from_doc(self.ui.caption_a.toHtml(), self.ui.caption_a.width() - 30)
            self.ui.caption_a.setHtml(doc_a)
            doc_b = resize_images_from_doc(self.ui.caption_b.toHtml(), self.ui.caption_b.width() - 30)
            self.ui.caption_b.setHtml(doc_b)
        except Exception:
            traceback.print_exc()

    def go_next(self):
        self.stages_stack.set_current_thesis(self.ui.rb_a.isChecked())
        if self.ui.rb_a.isChecked():
            stage = self.stages_stack.current_stage().thesis.target
        else:
            stage = self.stages_stack.current_stage().antithesis.target
        if isinstance(stage, Stage):  # Stage
            self.flag_on_ending = False
            self.stages_stack.add_stage(stage)
            self.display_current_stage()
        else:  # Ending
            self.flag_on_ending = True
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
        self.resize_images()
