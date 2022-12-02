import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QHBoxLayout, QVBoxLayout


class AccountSettingsWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Account Settings")

        # create main vertical layout
        main_layout = QtWidgets.QVBoxLayout()

        # create headline
        headline = QtWidgets.QLabel("Account Settings")
        main_layout.addWidget(headline)

        # create username header and textbox
        username_header = QtWidgets.QLabel("Username")
        username_textbox = QtWidgets.QLineEdit()
        main_layout.addWidget(username_header)
        main_layout.addWidget(username_textbox)

        # create password header and textbox
        password_header = QtWidgets.QLabel("Password")
        password_textbox = QtWidgets.QLineEdit()
        main_layout.addWidget(password_header)
        main_layout.addWidget(password_textbox)

        # create save directory header and textbox
        save_dir_header = QtWidgets.QLabel("Save Directory")
        save_dir_textbox = QtWidgets.QLineEdit()
        main_layout.addWidget(save_dir_header)
        main_layout.addWidget(save_dir_textbox)

        # create horizontal layout for select devices and update devices button
        devices_layout = QtWidgets.QHBoxLayout()
        # create select devices header and dropdown list
        select_devices_header = QtWidgets.QLabel("Select Devices")
        select_devices_list = QtWidgets.QComboBox()
        devices_layout.addWidget(select_devices_header)
        devices_layout.addWidget(select_devices_list)
        # create update devices button
        update_devices_button = QtWidgets.QPushButton("Update Devices")
        devices_layout.addWidget(update_devices_button)
        main_layout.addLayout(devices_layout)

        # create save account settings button
        save_button = QtWidgets.QPushButton("Save Account Settings")
        main_layout.addWidget(save_button)

        # set main layout
        self.setLayout(main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    account_settings_widget = AccountSettingsWidget()
    account_settings_widget.show()
    sys.exit(app.exec_())
