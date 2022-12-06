import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QHBoxLayout, QVBoxLayout, \
    QMessageBox

import config_tool


class AccountSettingsWidget(QWidget):
    def __init__(self, downloading_widget=None):
        super().__init__()

        self.downloading_widget = downloading_widget

        self.setWindowTitle("Account Settings")

        # create main vertical layout
        main_layout = QtWidgets.QVBoxLayout()

        # create headline
        headline = QtWidgets.QLabel("Account Settings")
        main_layout.addWidget(headline)

        # create username header and textbox
        username_header = QtWidgets.QLabel("Username")
        self.username_textbox = QtWidgets.QLineEdit()
        main_layout.addWidget(username_header)
        main_layout.addWidget(self.username_textbox)

        # create password header and textbox
        password_header = QtWidgets.QLabel("Password")
        self.password_textbox = QtWidgets.QLineEdit()
        main_layout.addWidget(password_header)
        main_layout.addWidget(self.password_textbox)

        save_dir_layout = QtWidgets.QHBoxLayout()
        # create save directory header and textbox
        save_dir_header = QtWidgets.QLabel("Save Directory")
        self.save_dir_textbox = QtWidgets.QLineEdit()
        self.save_dir_textbox.setText('vas_save')
        save_dir_layout.addWidget(save_dir_header)
        save_dir_layout.addWidget(self.save_dir_textbox)
        select_dir_button = QtWidgets.QPushButton("Select Path")
        select_dir_button.clicked.connect(self.select_dir_click)
        save_dir_layout.addWidget(select_dir_button)
        main_layout.addLayout(save_dir_layout)

        # create horizontal layout for select devices and update devices button
        devices_layout = QtWidgets.QHBoxLayout()
        # create select devices header and dropdown list
        select_devices_header = QtWidgets.QLabel("Select Devices")
        self.select_devices_list = QtWidgets.QComboBox()
        self.select_devices_list.addItem('All')
        devices_layout.addWidget(select_devices_header)
        devices_layout.addWidget(self.select_devices_list)
        # create update devices button
        update_devices_button = QtWidgets.QPushButton("Update Devices")
        devices_layout.addWidget(update_devices_button)
        main_layout.addLayout(devices_layout)

        # create save account settings button
        save_button = QtWidgets.QPushButton("Save Account Settings")
        save_button.clicked.connect(self.save_click)
        main_layout.addWidget(save_button)

        # set main layout
        self.setLayout(main_layout)

    def save_click(self):
        if not self.username_textbox.text():
            self.msg_box = QMessageBox()
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.setText("Username is empty. Please put your username!")
            self.msg_box.setStandardButtons(QMessageBox.Ok)
            self.msg_box.show()

        elif not self.password_textbox.text():
            self.msg_box = QMessageBox()
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.setText("Password is empty. Please put your password!")
            self.msg_box.setStandardButtons(QMessageBox.Ok)
            self.msg_box.show()

        elif config_tool.check_account_exist(self.username_textbox.text()):
            self.msg_box = QMessageBox()
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.setText("Username existed. Try modify the existing one at Downloading page.")
            self.msg_box.setStandardButtons(QMessageBox.Ok)
            self.msg_box.show()

        else:
            config_tool.save_account(
                account=self.username_textbox.text(),
                password=self.password_textbox.text(),
                save_dir=self.save_dir_textbox.text(),
                device=self.select_devices_list.currentText()
            )
            self.close()
            self.downloading_widget.load_accounts()

    def select_dir_click(self):
        folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
        self.save_dir_textbox.setText(folder_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    account_settings_widget = AccountSettingsWidget(None)
    account_settings_widget.show()
    sys.exit(app.exec_())
