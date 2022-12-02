from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QPushButton, QVBoxLayout, QHBoxLayout

from account import AccountSettingsWidget


class DownloadingWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # create headline label
        headline_label = QtWidgets.QLabel("Downloading")

        def add_account():
            self.account_window = AccountSettingsWidget()
            self.account_window.show()

        def add_session():
            pass

        # create list widgets and buttons
        list_widget1 = QtWidgets.QListWidget()
        list_widget2 = QtWidgets.QListWidget()
        button1 = QtWidgets.QPushButton("Add Account")
        button1.clicked.connect(add_account)
        button2 = QtWidgets.QPushButton("Add Session")
        button2.clicked.connect(add_session)

        # add checkboxes to list widgets
        for i in range(3):
            item1 = QtWidgets.QListWidgetItem()
            item1.setFlags(item1.flags() | QtCore.Qt.ItemIsUserCheckable)
            item1.setCheckState(QtCore.Qt.Unchecked)
            list_widget1.addItem(item1)

            item2 = QtWidgets.QListWidgetItem()
            item2.setFlags(item2.flags() | QtCore.Qt.ItemIsUserCheckable)
            item2.setCheckState(QtCore.Qt.Unchecked)
            list_widget2.addItem(item2)

        # create horizontal layouts
        layout1 = QtWidgets.QHBoxLayout()
        layout1.addWidget(list_widget1)
        layout1.addWidget(button1)

        layout2 = QtWidgets.QHBoxLayout()
        layout2.addWidget(list_widget2)
        layout2.addWidget(button2)

        # create start downloading button
        start_button = QtWidgets.QPushButton("Start downloading")

        # create main layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(headline_label)
        main_layout.addLayout(layout1)
        main_layout.addLayout(layout2)
        main_layout.addWidget(start_button)

        # set main layout
        self.setLayout(main_layout)