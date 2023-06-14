# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt_generated/settings.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SettingsForm(object):
    def setupUi(self, SettingsForm):
        SettingsForm.setObjectName("SettingsForm")
        SettingsForm.setWindowModality(QtCore.Qt.ApplicationModal)
        SettingsForm.resize(600, 400)
        SettingsForm.setMinimumSize(QtCore.QSize(600, 400))
        SettingsForm.setMaximumSize(QtCore.QSize(600, 400))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/img/img/b_logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        SettingsForm.setWindowIcon(icon)
        SettingsForm.setStyleSheet("")
        self.verticalLayout = QtWidgets.QVBoxLayout(SettingsForm)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(SettingsForm)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("")
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.rels_lineedit = QtWidgets.QLineEdit(SettingsForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.setHeightForWidth(self.rels_lineedit.sizePolicy().hasHeightForWidth())
        self.rels_lineedit.setSizePolicy(sizePolicy)
        self.rels_lineedit.setMinimumSize(QtCore.QSize(0, 25))
        self.rels_lineedit.setMaximumSize(QtCore.QSize(16777215, 25))
        self.rels_lineedit.setObjectName("rels_lineedit")
        self.verticalLayout.addWidget(self.rels_lineedit)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.save_button = QtWidgets.QPushButton(SettingsForm)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.save_button.setFont(font)
        self.save_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.save_button.setStyleSheet("")
        self.save_button.setObjectName("save_button")
        self.horizontalLayout.addWidget(self.save_button)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(SettingsForm)
        QtCore.QMetaObject.connectSlotsByName(SettingsForm)

    def retranslateUi(self, SettingsForm):
        _translate = QtCore.QCoreApplication.translate
        SettingsForm.setWindowTitle(_translate("SettingsForm", "Bionic - Settings"))
        self.label.setText(_translate("SettingsForm", "Books repository - rels.json"))
        self.save_button.setText(_translate("SettingsForm", "Save"))
from application.ui.qt_generated import res_rc
