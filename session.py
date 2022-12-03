import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QHBoxLayout, QVBoxLayout


class SessionSettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Session Widget")

        # create main vertical layout
        main_layout = QtWidgets.QVBoxLayout()

        # create headline
        headline = QtWidgets.QLabel("Session Settings")
        main_layout.addWidget(headline)

        # create date from layout
        date_from_layout = QtWidgets.QHBoxLayout()
        date_from_label = QtWidgets.QLabel("Date from")
        date_from_box = QtWidgets.QDateTimeEdit(calendarPopup=True)
        date_from_box.setDateTime(QtCore.QDateTime.currentDateTime())
        date_from_layout.addWidget(date_from_label)
        date_from_layout.addWidget(date_from_box)
        main_layout.addLayout(date_from_layout)

        # create date to layout
        date_to_layout = QtWidgets.QHBoxLayout()
        date_to_label = QtWidgets.QLabel("Date to")
        date_to_box = QtWidgets.QDateTimeEdit(calendarPopup=True)
        date_to_box.setDateTime(QtCore.QDateTime.currentDateTime())
        date_to_layout.addWidget(date_to_label)
        date_to_layout.addWidget(date_to_box)
        main_layout.addLayout(date_to_layout)

        # create save date and time checkbox layout
        save_date_time_layout = QtWidgets.QHBoxLayout()
        save_date_time_label = QtWidgets.QLabel("Save date and time in the transcript")
        save_date_time_checkbox = QtWidgets.QCheckBox()
        save_date_time_layout.addWidget(save_date_time_label)
        save_date_time_layout.addWidget(save_date_time_checkbox)
        main_layout.addLayout(save_date_time_layout)

        # create save device name checkbox layout
        save_device_name_layout = QtWidgets.QHBoxLayout()

        save_device_name_label = QtWidgets.QLabel("Save device name in the transcript")
        save_device_name_checkbox = QtWidgets.QCheckBox()
        save_device_name_layout.addWidget(save_device_name_label)
        save_device_name_layout.addWidget(save_device_name_checkbox)
        main_layout.addLayout(save_device_name_layout)
        # create save button
        save_button = QtWidgets.QPushButton("Save session settings")
        main_layout.addWidget(save_button)

        # set main layout
        self.setLayout(main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    account_settings_widget = SessionSettingsWidget()
    account_settings_widget.show()
    sys.exit(app.exec_())
