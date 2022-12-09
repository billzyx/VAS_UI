import os
from time import sleep
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QThread, QObject, pyqtSignal
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox

from account import AccountSettingsWidget
from session import SessionSettingsWidget

import config_tool


class DownloadingWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # create headline label
        headline_label = QtWidgets.QLabel("Downloading")
        headline_label.setObjectName("headline_label")
        # create list widgets and buttons
        self.list_widget_account = AccountSessionQListWidget(self.modify_account_click, self.delete_account)
        self.list_widget_account.setMinimumSize(800,400)
        self.list_widget_session = AccountSessionQListWidget(self.modify_session_click, self.delete_session)
        self.list_widget_session.setMinimumSize(800,400)

        button1 = QtWidgets.QPushButton("Add Account")
        button1.setObjectName('add_account')
        button1.setMinimumWidth(400)
        button1.clicked.connect(self.add_account_click)
        button2 = QtWidgets.QPushButton("Add Session")
        button2.setObjectName('add_session')
        button2.setMinimumWidth(400)
        button2.clicked.connect(self.add_session_click)

        self.load_accounts()
        self.load_sessions()

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

        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setObjectName("progress_bar")
        self.progress_bar.setVisible(0)

        # create start downloading button
        self.start_button = QtWidgets.QPushButton("Start downloading")
        # self.start_button.setFixedWidth(400)
        self.start_button.setObjectName("start_object_name")
        self.start_button.clicked.connect(self.start_downloading_click)

        self.download_status = QtWidgets.QLabel("")

        # create main layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(headline_label)
        main_layout.addLayout(layout1)
        main_layout.addLayout(layout2)
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.start_button)
        main_layout.addWidget(self.download_status)

        # set main layout
        self.setLayout(main_layout)

    def add_account_click(self):
        self.account_window = AccountSettingsWidget(self)
        self.account_window.show()

    def modify_account_click(self, item):
        self.account_window = AccountSettingsWidget(self, item)
        self.account_window.show()

    def add_session_click(self):
        self.session_window = SessionSettingsWidget(self)
        self.session_window.show()

    def modify_session_click(self, item):
        self.session_window = SessionSettingsWidget(self, item)
        self.session_window.show()

    def delete_account(self, account_str):
        config_tool.delete_account(account_str)
        self.load_accounts()

    def delete_session(self, session_name):
        config_tool.delete_session(session_name)
        self.load_sessions()

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

    def load_sessions(self):
        session_list = config_tool.load_sessions()
        self.list_widget_session.clear()
        # add checkboxes to list widgets
        for session in session_list:
            item1 = QtWidgets.QListWidgetItem()
            item1.setFlags(item1.flags() | QtCore.Qt.ItemIsUserCheckable)
            item1.setCheckState(QtCore.Qt.Unchecked)
            item1.setText(session['session_name'])
            self.list_widget_session.addItem(item1)

    def start_downloading_click(self):
        account_list = []
        for index in range(self.list_widget_account.count()):
            if self.list_widget_account.item(index).checkState() == Qt.Checked:
                account_list.append(config_tool.load_account(self.list_widget_account.item(index).text()))

        session_list = []
        for index in range(self.list_widget_session.count()):
            if self.list_widget_session.item(index).checkState() == Qt.Checked:
                session_list.append(config_tool.load_session(self.list_widget_session.item(index).text()))

        print(account_list)
        print(session_list)

        if not account_list:
            self.msg_box = QMessageBox()
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.setText("You need select at least one account to download!")
            self.msg_box.setStandardButtons(QMessageBox.Ok)
            self.msg_box.show()
            return

        if not session_list:
            self.msg_box = QMessageBox()
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.setText("You need select at least one session to download!")
            self.msg_box.setStandardButtons(QMessageBox.Ok)
            self.msg_box.show()
            return

        config_file_path_list = config_tool.generate_download_configs(account_list, session_list)

        if config_tool.check_downloading_exist(config_file_path_list):
            self.progress_bar.setVisible(1)
            self.start_download(config_file_path_list)
        else:
            self.msg_box = QMessageBox()
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.setText("One of the session already downloaded. If you need re-download,"
                                 " please delete the corresponding fonder under your Save Directory")
            self.msg_box.setStandardButtons(QMessageBox.Ok)
            self.msg_box.show()
            return

    def start_download(self, config_file_path_list):
        self.start_button.setEnabled(False)  # Disable the start button
        self.worker = MyWorker(config_file_path_list)  # Create the worker
        # Connect the signal from the worker to the progress bar
        self.worker.update_progress.connect(self.progress_bar.setValue)
        # Connect the finished signal to a slot
        self.worker.finished.connect(self.on_finished)
        self.progress_bar.setRange(0, len(config_file_path_list))

        self.thread = QtCore.QThread()  # Create a new thread
        self.worker.moveToThread(self.thread)  # Move the worker to the new thread
        self.thread.started.connect(self.worker.run)  # Start the worker when the thread starts
        self.thread.start()  # Start the thread

    @QtCore.pyqtSlot()
    def on_finished(self):
        self.start_button.setEnabled(True)  # Enable the start button
        self.download_status.setText("Downloading finished")  # Change the text of the button


class MyWorker(QtCore.QObject):
    # Signal that will be emitted during the process
    update_progress = QtCore.pyqtSignal(int)
    finished = QtCore.pyqtSignal()

    def __init__(self, config_file_path_list):
        super().__init__(None)
        self.config_file_path_list = config_file_path_list

    @QtCore.pyqtSlot()
    def run(self):
        # This is the code that will run in the new thread
        for i, config_file_path in enumerate(self.config_file_path_list):
            if i > 0:
                sleep(10)
            cmd = 'python3 vas-toolkit/alexa.py --config_file_path {}'.format(config_file_path)
            os.system(cmd)
            self.update_progress.emit(i + 1)
        self.finished.emit()


class AccountSessionQListWidget(QListWidget):
    def __init__(self, modify_click, delete_click):
        super().__init__()

        self.setToolTip('Double click to modify')
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_right_click_list_widget)
        self.itemDoubleClicked.connect(modify_click)
        self.delete_function = delete_click

    def on_right_click_list_widget(self, pos):
        # Get the index of the item that was right-clicked
        index = self.indexAt(pos)

        if not index.isValid():  # Check if a valid item was right-clicked
            return

        item = self.itemFromIndex(index)  # Get the item
        text = item.text()  # Get the text of the item

        # Create a context menu with two options
        menu = QtWidgets.QMenu()
        option1 = menu.addAction("Delete")

        # Show the context menu
        action = menu.exec_(self.viewport().mapToGlobal(pos))

        if action == option1:  # If the user selected option 1
            print("Selected for item:", text)
            result = QMessageBox.question(None, "Confirmation", "Are you sure to delete {} ?".format(text),
                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            # Check the result of the dialog and act accordingly.
            if result == QMessageBox.Yes:
                self.delete_function(text)

