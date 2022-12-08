import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QPushButton, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget, \
    QTableWidget, QTableWidgetItem, QCheckBox, QMessageBox, QAbstractItemView, QTableWidgetSelectionRange

import transctipt_tools


class VisualizationWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Create a QTabWidget
        self.tabs = QTabWidget()

        # Enable the close button on the tabs
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)

        # Connect the tabCloseRequested signal to the close_tab slot
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.tabBarDoubleClicked.connect(self.add_tab)

        # Create a button to add new tabs
        self.add_button = QPushButton("Add Tab")

        # Connect the clicked signal to the add_tab slot
        self.add_button.clicked.connect(self.add_tab)

        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.add_button)
        layout.addWidget(self.tabs)

        self.setLayout(layout)

        self.tab_count = 0

        # Add a few tabs
        for i in range(1):
            self.tabs_count = 0
            self.tabs.addTab(VisualizationTab(), "Tab {}".format(i))

    def close_tab(self, index):
        # Get the widget for the tab
        widget = self.tabs.widget(index)

        # Remove the widget and the tab
        widget.deleteLater()
        self.tabs.removeTab(index)

    def add_tab(self):
        # Add a new tab with a default name
        self.tabs_count += 1
        self.tabs.addTab(VisualizationTab(), "Tab {}".format(self.tabs_count))


class VisualizationTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # create main horizontal layout
        self.main_layout = QtWidgets.QVBoxLayout()

        # create play/stop button horizontal layout
        play_button_layout = QtWidgets.QHBoxLayout()
        self.play_button = QtWidgets.QPushButton("Play")
        self.play_button.clicked.connect(self.play_click)
        stop_button = QtWidgets.QPushButton("Stop")
        stop_button.clicked.connect(self.stop_click)
        play_button_layout.addWidget(self.play_button)
        play_button_layout.addWidget(stop_button)
        self.main_layout.addLayout(play_button_layout)

        # create open button
        self.content_layout = QtWidgets.QVBoxLayout()
        self.content_layout.addStretch()
        open_button_layout = QtWidgets.QVBoxLayout()
        open_button_layout.setAlignment(Qt.AlignCenter)
        open_button_layout.addStretch()
        open_button = QtWidgets.QPushButton("Open")
        open_button.setFixedSize(100, 50)
        open_button.clicked.connect(self.open_action)
        open_button_layout.addWidget(open_button)

        # create placeholder text
        placeholder_text = QtWidgets.QLabel(".cha or .txt file")
        open_button_layout.addWidget(placeholder_text)
        open_button_layout.addStretch()
        self.content_layout.addLayout(open_button_layout)
        self.content_layout.addStretch()

        self.main_layout.addLayout(self.content_layout)

        # set main layout
        self.setLayout(self.main_layout)

        self.player = QMediaPlayer()
        self.table_widget = None
        self.audio_list = []
        self.current_audio = 0

    def open_action(self):
        file_path = QtWidgets.QFileDialog.getOpenFileName(
            self, caption='Select .txt or .cha file', filter='VAS Transcript Files (*.txt *.cha)')
        print(file_path[0])
        try:
            self.table_widget = TableWidget(file_path[0])
        except:
            self.msg_box = QMessageBox()
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.setText("Load failed. Check if it is a VAS transcript file!")
            self.msg_box.setStandardButtons(QMessageBox.Ok)
            self.msg_box.show()
            return
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget() is not None:
                item.widget().deleteLater()
            elif item.layout() is not None:
                item.layout().deleteLater()
        self.content_layout.addWidget(self.table_widget)

    def play_click(self):
        if self.play_button.text() == 'Play':
            if not self.table_widget:
                self.msg_box = QMessageBox()
                self.msg_box.setIcon(QMessageBox.Warning)
                self.msg_box.setText("Open a file first!")
                self.msg_box.setStandardButtons(QMessageBox.Ok)
                self.msg_box.show()
                return
            # try:
            if self.table_widget.file_path.endswith('.txt'):
                self.play_txt()
            elif self.table_widget.file_path.endswith('.cha'):
                self.play_cha()
            # except:
            #     self.msg_box = QMessageBox()
            #     self.msg_box.setIcon(QMessageBox.Warning)
            #     self.msg_box.setText("Cannot find audio file!")
            #     self.msg_box.setStandardButtons(QMessageBox.Ok)
            #     self.msg_box.show()
            #     return
        elif self.play_button.text() == 'Pause':
            self.player.pause()
            self.play_button.setText('Continue Play')
        else:
            self.player.play()
            self.play_button.setText('Pause')

    def stop_click(self):
        if self.table_widget:
            self.player.stop()
            self.table_widget.cancel_highlight(self.current_audio)
            self.player = None
            self.play_button.setText("Play")

    def on_media_status_changed(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            # Set the next audio file to play
            self.play_next()

    def on_position_changed(self, position):
        # This callback will be called at regular intervals
        # during the playback of the audio file. The position
        # parameter indicates the current position of the
        # media player in milliseconds.
        end_time = int(self.audio_list[self.current_audio][1])
        if position >= end_time:
            self.player.pause()
            self.play_next()

    def play_next(self):
        if self.current_audio >= 0:
            self.table_widget.cancel_highlight(self.current_audio)
        self.current_audio += 1
        if self.current_audio >= len(self.audio_list):
            self.play_button.setText("Play")
            return
        if not self.audio_list[self.current_audio]:
            self.play_next()
            return

        if self.table_widget.file_path.endswith('.txt'):
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.audio_list[self.current_audio])))
        else:
            # play .cha
            start_time = int(self.audio_list[self.current_audio][0])
            self.player.setPosition(start_time)

        self.table_widget.set_highlight(self.current_audio)

        # Play the next audio file
        self.player.play()

    def play_txt(self):
        self.audio_list = []
        self.current_audio = -1
        self.player = QMediaPlayer()
        for idx, audio in enumerate(self.table_widget.audio_list):
            if audio:
                audio_path = os.path.join(os.path.dirname(self.table_widget.file_path), 'audio', audio)
                self.audio_list.append(audio_path)
            else:
                self.audio_list.append(None)
        self.player.mediaStatusChanged.connect(self.on_media_status_changed)
        self.play_button.setText("Pause")
        self.play_next()

    def play_cha(self):
        self.audio_list = []
        self.current_audio = -1
        self.player = QMediaPlayer()
        for idx, audio in enumerate(self.table_widget.audio_list):
            if audio:
                self.audio_list.append(audio.split('_'))
            else:
                self.audio_list.append(None)
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.table_widget.file_path.replace('.cha', '.wav'))))
        self.player.positionChanged.connect(self.on_position_changed)
        self.player.setNotifyInterval(10)
        self.play_button.setText("Pause")
        self.play_next()


class TableWidget(QtWidgets.QWidget):
    def __init__(self, file_path):
        super().__init__()
        self.setWindowTitle("Table Widget")

        self.table = QTableWidget()

        self.load_file(file_path)
        self.file_path = file_path

        # self.table.resizeColumnsToContents()
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.table.horizontalHeader().setStretchLastSection(True)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

    def load_file(self, file_path):
        assert file_path.endswith('.cha') or file_path.endswith('.txt')

        if file_path.endswith('.cha'):
            speaker_list, text_list, audio_list = transctipt_tools.load_cha_file(file_path)
        elif file_path.endswith('.txt'):
            speaker_list, text_list, audio_list = transctipt_tools.load_txt_file(file_path)

        self.audio_list = audio_list

        self.table.setRowCount(len(speaker_list))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Speaker', 'Text', 'Play'])

        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(1, 400)
        self.table.setColumnWidth(2, 100)

        for row in range(len(speaker_list)):
            self.table.setItem(row, 0, QTableWidgetItem(speaker_list[row]))
            self.table.setItem(row, 1, QTableWidgetItem(text_list[row]))

            self.table.resizeRowToContents(row)
            play_btn = QPushButton('Play')
            play_btn.setFixedSize(50, 30)
            self.table.setCellWidget(row, 2, play_btn)

    def set_highlight(self, row):
        self.table.setRangeSelected(QTableWidgetSelectionRange(row, 0, row, self.table.columnCount() - 1), True)
        self.table.setStyleSheet("QTableWidget::item:selected{background-color: blue;}")

    def cancel_highlight(self, row):
        self.table.setRangeSelected(QTableWidgetSelectionRange(row, 0, row, self.table.columnCount() - 1), False)
