import os


def update_pyqt_files():
    cwd = os.getcwd()
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    os.system("pyrcc5 -o qt_generated/res_rc.py ../res.qrc")

    os.system("pyuic5 -o qt_generated/main_window.py --import-from='application.ui.qt_generated' qt_generated/main_window.ui")
    os.system("pyuic5 -o qt_generated/add_dialog.py --import-from='application.ui.qt_generated' qt_generated/add_dialog.ui")
    os.system("pyuic5 -o qt_generated/determinant.py --import-from='application.ui.qt_generated' qt_generated/determinant.ui")
    os.system("pyuic5 -o qt_generated/entry_points.py --import-from='application.ui.qt_generated' qt_generated/entry_points.ui")
    os.system("pyuic5 -o qt_generated/itembook_widget.py --import-from='application.ui.qt_generated' qt_generated/itembook_widget.ui")
    os.system("pyuic5 -o qt_generated/result.py --import-from='application.ui.qt_generated' qt_generated/result.ui")
    os.system("pyuic5 -o qt_generated/settings.py --import-from='application.ui.qt_generated' qt_generated/settings.ui")

    os.system("pyuic5 -o qt_generated/dark/dark_main_window.py --import-from='application.ui.qt_generated' qt_generated/dark/dark_main_window.ui")
    os.system("pyuic5 -o qt_generated/dark/dark_add_dialog.py --import-from='application.ui.qt_generated' qt_generated/dark/dark_add_dialog.ui")
    os.system("pyuic5 -o qt_generated/dark/dark_determinant.py --import-from='application.ui.qt_generated' qt_generated/dark/dark_determinant.ui")
    os.system("pyuic5 -o qt_generated/dark/dark_entry_points.py --import-from='application.ui.qt_generated' qt_generated/dark/dark_entry_points.ui")
    os.system("pyuic5 -o qt_generated/dark/dark_itembook_widget.py --import-from='application.ui.qt_generated' qt_generated/dark/dark_itembook_widget.ui")
    os.system("pyuic5 -o qt_generated/dark/dark_result.py --import-from='application.ui.qt_generated' qt_generated/dark/dark_result.ui")
    os.system("pyuic5 -o qt_generated/dark/dark_settings.py --import-from='application.ui.qt_generated' qt_generated/dark/dark_settings.ui")

    os.chdir(cwd)


if __name__ == '__main__':
    update_pyqt_files()
