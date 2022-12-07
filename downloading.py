from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QPushButton, QVBoxLayout, QHBoxLayout

from account import AccountSettingsWidget
from session import SessionSettingsWidget

import config_tool


class DownloadingWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # create headline label
        headline_label = QtWidgets.QLabel("Downloading")

        # create list widgets and buttons
        self.list_widget_account = QtWidgets.QListWidget()
        self.list_widget_account.setToolTip('Double click to modify')
        self.list_widget_account.itemDoubleClicked.connect(self.modify_account_click)
        self.list_widget_session = QtWidgets.QListWidget()
        button1 = QtWidgets.QPushButton("Add Account")
        button1.clicked.connect(self.add_account_click)
        button2 = QtWidgets.QPushButton("Add Session")
        button2.clicked.connect(self.add_session_click)

        self.load_accounts()

        # # add checkboxes to list widgets
        # for i in range(3):
        #     item1 = QtWidgets.QListWidgetItem()
        #     item1.setFlags(item1.flags() | QtCore.Qt.ItemIsUserCheckable)
        #     item1.setCheckState(QtCore.Qt.Unchecked)
        #     list_widget_account.addItem(item1)
        #
        #     item2 = QtWidgets.QListWidgetItem()
        #     item2.setFlags(item2.flags() | QtCore.Qt.ItemIsUserCheckable)
        #     item2.setCheckState(QtCore.Qt.Unchecked)
        #     list_widget_session.addItem(item2)

        # create horizontal layouts
        layout1 = QtWidgets.QHBoxLayout()
        layout1.addWidget(self.list_widget_account)
        layout1.addWidget(button1)

        layout2 = QtWidgets.QHBoxLayout()
        layout2.addWidget(self.list_widget_session)
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

    def add_account_click(self):
        self.account_window = AccountSettingsWidget(self)
        self.account_window.show()

    def modify_account_click(self, item):
        self.account_window = AccountSettingsWidget(self, item)
        self.account_window.show()

    def add_session_click(self):
        self.account_window = SessionSettingsWidget()
        self.account_window.show()

    def load_accounts(self):
        account_list = config_tool.load_accounts()
        self.list_widget_account.clear()
        # add checkboxes to list widgets
        for account in account_list:
            item1 = QtWidgets.QListWidgetItem()
            item1.setFlags(item1.flags() | QtCore.Qt.ItemIsUserCheckable)
            item1.setCheckState(QtCore.Qt.Unchecked)
            item1.setText(account['account'])
            self.list_widget_account.addItem(item1)
