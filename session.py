import sys
from datetime import datetime

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QHBoxLayout, QVBoxLayout, \
    QMessageBox

import config_tool


class SessionSettingsWidget(QWidget):
    def __init__(self, downloading_widget=None, list_widget_item=None):
        super().__init__()
        self.setWindowTitle("Session Widget")
        # self.setMinimumSize(700, 950)
        # self.setMaximumSize(700, 950)

        self.downloading_widget = downloading_widget
        self.list_widget_item = list_widget_item

        # create main vertical layout
        main_layout = QtWidgets.QVBoxLayout()

        # create headline
        headline = QtWidgets.QLabel("Session Settings")
        main_layout.addWidget(headline)
        headline.setObjectName("session_headline")

        # create session_name header and textbox
        session_name_header = QtWidgets.QLabel("Session name")
        # session_name_header.setObjectName('session_name_header')
        self.session_name_textbox = QtWidgets.QLineEdit()
        self.session_name_textbox.setObjectName('session_name_editor')
        self.session_name_textbox.setText('{}_new_session'.format(datetime.today().strftime("%Y-%m-%d-%H-%M-%S")))
        main_layout.addWidget(session_name_header)
        session_name_header.setObjectName("session_name_header")
        main_layout.addWidget(self.session_name_textbox)

        # create date from layout
        # date_from_layout = QtWidgets.QHBoxLayout()
        date_from_label = QtWidgets.QLabel("Date from")
        date_from_label.setObjectName('date_from_label')
        self.date_from_box = QtWidgets.QDateTimeEdit(calendarPopup=True)
        self.date_from_box.setDateTime(QtCore.QDateTime.currentDateTime())
        main_layout.addWidget(date_from_label)
        main_layout.addWidget(self.date_from_box)
        # main_layout.addLayout(date_from_layout)

        # create date to layout
        # date_to_layout = QtWidgets.QHBoxLayout()
        date_to_label = QtWidgets.QLabel("Date to")
        date_to_label.setObjectName('date_to_label')
        self.date_to_box = QtWidgets.QDateTimeEdit(calendarPopup=True)
        self.date_to_box.setDateTime(QtCore.QDateTime.currentDateTime())
        main_layout.addWidget(date_to_label)
        main_layout.addWidget(self.date_to_box)
        # main_layout.addLayout(date_to_layout)

        # create save date and time checkbox layout
        save_date_time_layout = QtWidgets.QHBoxLayout()
        save_date_time_label = QtWidgets.QLabel("Save date and time in the transcript")
        save_date_time_label.setObjectName('save_date_time_label')
        self.save_date_time_checkbox = QtWidgets.QCheckBox()
        save_date_time_layout.addWidget(save_date_time_label)
        save_date_time_layout.addWidget(self.save_date_time_checkbox)
        save_date_time_layout.setContentsMargins(0, 30, 0, 20)
        main_layout.addLayout(save_date_time_layout)

        # create save device name checkbox layout
        save_device_name_layout = QtWidgets.QHBoxLayout()

        save_device_name_label = QtWidgets.QLabel("Save device name in the transcript")
        save_device_name_label.setObjectName('save_device_name_label')
        self.save_device_name_checkbox = QtWidgets.QCheckBox()
        save_device_name_layout.addWidget(save_device_name_label)
        save_device_name_layout.addWidget(self.save_device_name_checkbox)
        save_device_name_layout.setContentsMargins(0, 20, 0, 0)
        main_layout.addLayout(save_device_name_layout)
        # create save button
        save_button = QtWidgets.QPushButton("Save session settings")
        save_button.clicked.connect(self.save_click)
        save_button.setObjectName("save_button")
        main_layout.addWidget(save_button)

        # set main layout
        self.setLayout(main_layout)

        if self.list_widget_item:
            self.session = self.list_widget_item.text()
            self.load_session()

    def save_click(self):
        if not self.session_name_textbox.text():
            self.msg_box = QMessageBox()
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.setText("Session name is empty. Please put your session name!")
            self.msg_box.setStandardButtons(QMessageBox.Ok)
            self.msg_box.show()
            return

        if not self.list_widget_item:
            if config_tool.check_session_exist(self.session_name_textbox.text()):
                self.msg_box = QMessageBox()
                self.msg_box.setIcon(QMessageBox.Warning)
                self.msg_box.setText("Session name existed. Try modify the existing one at the Downloading page.")
                self.msg_box.setStandardButtons(QMessageBox.Ok)
                self.msg_box.show()
                return

        if self.date_from_box.dateTime() > self.date_to_box.dateTime():
            self.msg_box = QMessageBox()
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.setText("You Date to is earlier than Date from. Try a earlier Date from!")
            self.msg_box.setStandardButtons(QMessageBox.Ok)
            self.msg_box.show()
            return

        if self.list_widget_item:
            config_tool.delete_session(self.session)

        config_tool.save_session(
            session_name=self.session_name_textbox.text(),
            date_from=self.date_from_box.date().toPyDate().strftime("%m/%d/%Y"),
            date_to=self.date_to_box.date().toPyDate().strftime("%m/%d/%Y"),
            time_from=self.date_from_box.time().toPyTime().strftime("%H:%M"),
            time_to=self.date_to_box.time().toPyTime().strftime("%H:%M"),
            save_date_time=self.save_date_time_checkbox.isChecked(),
            save_device_name=self.save_device_name_checkbox.isChecked(),
        )
        self.close()
        self.downloading_widget.load_sessions()

    def load_session(self):
        session_dict = config_tool.load_session(self.session)
        self.session_name_textbox.setText(session_dict['session_name'])
        self.date_from_box.setDate(datetime.strptime(session_dict['date_from'], "%m/%d/%Y").date())
        self.date_to_box.setDate(datetime.strptime(session_dict['date_to'], "%m/%d/%Y").date())
        self.date_from_box.setTime(datetime.strptime(session_dict['time_from'], "%H:%M").time())
        self.date_to_box.setTime(datetime.strptime(session_dict['time_to'], "%H:%M").time())
        self.save_date_time_checkbox.setChecked(session_dict['save_date_time'])
        self.save_device_name_checkbox.setChecked(session_dict['save_device_name'])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    session_settings_widget = SessionSettingsWidget()
    session_settings_widget.show()
    with open("style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)
    sys.exit(app.exec_())
