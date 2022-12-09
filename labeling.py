import os
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QPushButton, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget, \
    QTableWidget, QTableWidgetItem, QCheckBox, QMessageBox, QAbstractItemView, QTableWidgetSelectionRange, QStyle

from vis_tab import VisTab


class LabelingWidget(QtWidgets.QWidget):
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
        self.add_button.setObjectName('add_tab')

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
            self.tabs.addTab(VisTab(self, mode='labeling'), "Tab {}".format(i))

    def close_tab(self, index):
        # Get the widget for the tab
        widget = self.tabs.widget(index)

        # Remove the widget and the tab
        widget.deleteLater()
        self.tabs.removeTab(index)

    def add_tab(self):
        # Add a new tab with a default name
        self.tabs_count += 1
        self.tabs.addTab(VisTab(self, mode='labeling'), "Tab {}".format(self.tabs_count))
