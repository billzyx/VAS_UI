from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QPushButton, QVBoxLayout, QHBoxLayout, QTabWidget


class VisualizationWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        tabs = QTabWidget()

        # Add tabs
        tabs.addTab(VisualizationTab(), "First Tab")
        tabs.addTab(VisualizationTab(), "Second Tab")

        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(tabs)
        self.setLayout(layout)


class VisualizationTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # create main horizontal layout
        main_layout = QtWidgets.QVBoxLayout()

        # create play/stop button horizontal layout
        play_button_layout = QtWidgets.QHBoxLayout()
        play_button = QtWidgets.QPushButton("Play")
        stop_button = QtWidgets.QPushButton("Stop")
        play_button_layout.addWidget(play_button)
        play_button_layout.addWidget(stop_button)
        main_layout.addLayout(play_button_layout)

        # create open button
        content_layout = QtWidgets.QVBoxLayout()
        content_layout.addStretch()
        open_button_layout = QtWidgets.QVBoxLayout()
        open_button_layout.setAlignment(Qt.AlignCenter)
        open_button_layout.addStretch()
        open_button = QtWidgets.QPushButton("Open")
        open_button.setFixedSize(100, 50)
        open_button_layout.addWidget(open_button)

        # create placeholder text
        placeholder_text = QtWidgets.QLabel(".cha or .txt file")
        open_button_layout.addWidget(placeholder_text)
        open_button_layout.addStretch()
        content_layout.addLayout(open_button_layout)
        content_layout.addStretch()

        main_layout.addLayout(content_layout)

        # set main layout
        self.setLayout(main_layout)


