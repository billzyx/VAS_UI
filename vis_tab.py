import os
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QPushButton, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget, \
    QTableWidget, QTableWidgetItem, QCheckBox, QMessageBox, QAbstractItemView, QTableWidgetSelectionRange, QStyle

import transctipt_tools


class VisTab(QtWidgets.QWidget):
    def __init__(self, parent_vis_widget, mode='visualization'):
        super().__init__()

        self.parent_vis_widget = parent_vis_widget
        self.mode = mode

        # create main horizontal layout
        self.main_layout = QtWidgets.QVBoxLayout()

        # create play/stop button horizontal layout
        play_button_layout = QtWidgets.QHBoxLayout()
        self.play_button = QtWidgets.QPushButton("Play")
        self.play_button.setIcon(self.play_button.style().standardIcon(getattr(QStyle, "SP_MediaPlay")))
        # self.play_button.setIcon(QtGui.QIcon('assets/images/play-button.png'))
        self.play_button.setObjectName("icon_btn")
        self.play_button.clicked.connect(self.play_click)
        stop_button = QtWidgets.QPushButton("Stop")
        stop_button.setIcon(stop_button.style().standardIcon(getattr(QStyle, "SP_MediaStop")))
        stop_button.setObjectName("icon_btn")
        stop_button.clicked.connect(self.stop_click)
        play_button_layout.addWidget(self.play_button)
        play_button_layout.addWidget(stop_button)

        if mode == 'labeling':
            self.save_button = QtWidgets.QPushButton("Save")
            self.play_button.clicked.connect(self.save_click)
            play_button_layout.addWidget(self.save_button)

        self.main_layout.addLayout(play_button_layout)

        # create open button
        self.content_layout = QtWidgets.QVBoxLayout()
        self.content_layout.addStretch()
        open_button_layout = QtWidgets.QVBoxLayout()
        open_button_layout.setAlignment(Qt.AlignCenter)
        open_button_layout.addStretch()
        open_button = QtWidgets.QPushButton("Open")
        open_button.setFixedSize(200, 75)
        open_button.setStyleSheet("font-size:12pt;")
        open_button.clicked.connect(self.open_action)
        open_button_layout.addWidget(open_button)

        # create placeholder text
        placeholder_text = QtWidgets.QLabel(".cha or .txt file")
        placeholder_text.setObjectName("light_text")
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
            self.table_widget = VisTableWidget(file_path[0], self)
            self.table_widget.table.itemDoubleClicked.connect(self.table_item_double_click_play)
            self.parent_vis_widget.tabs.setTabText(
                self.parent_vis_widget.tabs.indexOf(self),
                '{}/{}'.format(os.path.basename(os.path.dirname(file_path[0])), os.path.basename(file_path[0])))
        except FileNotFoundError:
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
            self.play()
        elif self.play_button.text() == 'Pause':
            self.player.pause()
            self.play_button.setText('Continue Play')
            self.play_button.setIcon(self.play_button.style().standardIcon(getattr(QStyle, "SP_MediaPlay")))
        else:
            self.player.play()
            self.play_button.setText('Pause')
            self.play_button.setIcon(self.play_button.style().standardIcon(getattr(QStyle, "SP_MediaPause")))

    def table_item_double_click_play(self, item):
        self.play(item.row())

    def play(self, audio_idx=0, play_single_command=False):
        if play_single_command:
            self.play_button.setText('Play')
            self.play_button.setIcon(self.play_button.style().standardIcon(getattr(QStyle, "SP_MediaPlay")))
        try:
            if self.table_widget.file_path.endswith('.txt'):
                self.play_txt(audio_idx, play_single_command)
            elif self.table_widget.file_path.endswith('.cha'):
                self.play_cha(audio_idx, play_single_command)
        except FileNotFoundError:
            self.msg_box = QMessageBox()
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.setText("Cannot find the audio file!")
            self.msg_box.setStandardButtons(QMessageBox.Ok)
            self.msg_box.show()
            return

    def stop_click(self):
        if self.table_widget:
            if self.player:
                self.player.stop()
            self.table_widget.cancel_highlight(self.current_audio)
            self.player = None
            self.play_button.setText("Play")
            self.play_button.setIcon(self.play_button.style().standardIcon(getattr(QStyle, "SP_MediaPlay")))

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

    def on_position_changed_single(self, position):
        # This callback will be called at regular intervals
        # during the playback of the audio file. The position
        # parameter indicates the current position of the
        # media player in milliseconds.
        end_time = int(self.audio_list[self.current_audio][1])
        if position >= end_time:
            self.player.pause()

    def play_next(self):
        if self.current_audio >= 0:
            self.table_widget.cancel_highlight(self.current_audio)
        self.current_audio += 1
        if self.current_audio >= len(self.audio_list):
            self.play_button.setText("Play")
            self.play_button.setIcon(self.play_button.style().standardIcon(getattr(QStyle, "SP_MediaPlay")))
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

    def play_txt(self, audio_idx=0, play_single_command=False):
        self.audio_list = []
        self.current_audio = audio_idx - 1
        self.player = QMediaPlayer()
        for idx, audio in enumerate(self.table_widget.audio_list):
            if audio:
                audio_path = os.path.join(os.path.dirname(self.table_widget.file_path), 'audio', audio)
                if not os.path.isfile(audio_path):
                    raise FileNotFoundError
                self.audio_list.append(audio_path)
            else:
                self.audio_list.append(None)
        if play_single_command:
            self.current_audio += 1
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.audio_list[self.current_audio])))
            self.player.play()
            return
        self.player.mediaStatusChanged.connect(self.on_media_status_changed)
        self.play_button.setText("Pause")
        self.play_button.setIcon(self.play_button.style().standardIcon(getattr(QStyle, "SP_MediaPause")))
        self.play_next()

    def play_cha(self, audio_idx=0, play_single_command=False):
        self.audio_list = []
        self.current_audio = audio_idx - 1
        self.player = QMediaPlayer()
        for idx, audio in enumerate(self.table_widget.audio_list):
            if audio:
                self.audio_list.append(audio.split('_'))
            else:
                self.audio_list.append(None)
        audio_file_path = self.table_widget.file_path.replace('.cha', '.wav')
        if not os.path.isfile(audio_file_path):
            raise FileNotFoundError
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(audio_file_path)))
        self.player.setNotifyInterval(10)

        if play_single_command:
            self.current_audio += 1
            self.player.positionChanged.connect(self.on_position_changed_single)
            start_time = int(self.audio_list[self.current_audio][0])
            self.player.setPosition(start_time)
            self.player.play()
            return

        self.player.positionChanged.connect(self.on_position_changed)
        self.play_button.setText("Pause")
        self.play_button.setIcon(self.play_button.style().standardIcon(getattr(QStyle, "SP_MediaPause")))
        self.play_next()

    def save_click(self):
        pass


class VisTableWidget(QtWidgets.QWidget):
    def __init__(self, file_path, vis_tab):
        super().__init__()
        self.setWindowTitle("Table Widget")

        self.vis_tab = vis_tab

        self.table = QTableWidget()
        self.table.setToolTip('Double click to play')

        self.load_file(file_path)
        self.file_path = file_path

        # self.table.resizeColumnsToContents()
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.table.horizontalHeader().setStretchLastSection(True)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

    def load_file(self, file_path):
        if not (file_path.endswith('.cha') or file_path.endswith('.txt') or os.path.isfile(file_path)):
            raise FileNotFoundError

        if file_path.endswith('.cha'):
            speaker_list, text_list, audio_list = transctipt_tools.load_cha_file(file_path)
        elif file_path.endswith('.txt'):
            speaker_list, text_list, audio_list = transctipt_tools.load_txt_file(file_path)

        self.audio_list = audio_list

        self.table.setRowCount(len(speaker_list))

        if self.vis_tab.mode == 'visualization':
            self.table.setColumnCount(3)
            self.table.setHorizontalHeaderLabels(['Speaker', 'Text', 'Play'])
        elif self.vis_tab.mode == 'labeling':
            self.table.setColumnCount(7)
            self.table.setHorizontalHeaderLabels(['Speaker', 'Text', 'Play', 'Remove', 'Error', 'To PAR', 'To VAS'])
        else:
            raise ValueError('self.vis_tab.mode should be either visualization or labeling')

        # Set the horizontal header labels to be always visible
        self.table.horizontalHeader().setVisible(True)

        self.table.setColumnWidth(0, 230)
        self.table.setColumnWidth(1, 650)
        self.table.setColumnWidth(2, 120)

        for row in range(len(speaker_list)):
            self.table.setItem(row, 0, QTableWidgetItem(speaker_list[row]))
            self.table.setItem(row, 1, QTableWidgetItem(text_list[row]))
            self.table.resizeRowToContents(row)
            if audio_list[row]:
                play_btn = QPushButton("")
                play_btn.setFixedSize(200, 40)
                play_btn.setIcon(play_btn.style().standardIcon(getattr(QStyle, "SP_MediaPlay")))
                play_btn.setObjectName("play_btn")
                play_btn.clicked.connect(
                    lambda _, x=row: self.vis_tab.play(x, True))
                self.table.setCellWidget(row, 2, play_btn)

                if self.vis_tab.mode == 'labeling':
                    for col in range(3, 7):
                        checkbox = QtWidgets.QCheckBox()
                        self.table.setCellWidget(row, col, checkbox)

    def set_highlight(self, row):
        row_item = self.table.item(row, 0)
        # Get the coordinates of the first row in the viewport
        rect = self.table.visualItemRect(row_item)

        # Get the bounds of the viewport
        viewport = self.table.viewport().rect()

        # Check if the top and bottom coordinates of the row are within the bounds of the viewport
        if not (rect.top() >= viewport.top() and rect.bottom() <= viewport.bottom()):
            self.table.scrollToItem(row_item, QAbstractItemView.PositionAtCenter)

        self.table.setRangeSelected(QTableWidgetSelectionRange(row, 0, row, self.table.columnCount() - 1), True)
        self.table.setStyleSheet("QTableWidget::item:selected{background-color: blue;}")

    def cancel_highlight(self, row):
        self.table.setRangeSelected(QTableWidgetSelectionRange(row, 0, row, self.table.columnCount() - 1), False)
