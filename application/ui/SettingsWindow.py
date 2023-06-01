from PyQt5.QtWidgets import QWidget

from .qt_generated.settings import Ui_SettingsForm
from .qt_generated.dark.dark_settings import Ui_DarkSettingsForm


class SettingsForm(QWidget):
    def __init__(self, parent, config):
        super().__init__()
        self.parent_window = parent
        self.config = config
        self.ui = Ui_SettingsForm() if not int(self.config["dark_mode"]) else Ui_DarkSettingsForm()
        self.ui.setupUi(self)
        self.ui.save_button.clicked.connect(self.save_clicked)

    def showEvent(self, a0) -> None:
        a0.accept()
        self.move(self.parent_window.frameGeometry().center().x() - self.frameGeometry().width() / 2,
                  self.parent_window.frameGeometry().center().y() - self.frameGeometry().height() / 2)
        self.ui.rels_lineedit.setText(self.config["rels"])

    def save_clicked(self):
        self.config["rels"] = self.ui.rels_lineedit.text()
        self.config.save()
