from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QPushButton, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget


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
        play_button = QtWidgets.QPushButton("Play")
        stop_button = QtWidgets.QPushButton("Stop")
        play_button_layout.addWidget(play_button)
        play_button_layout.addWidget(stop_button)
        self.main_layout.addLayout(play_button_layout)

        # create open button
        self.content_layout = QtWidgets.QVBoxLayout()
        self.content_layout.addStretch()
        open_button_layout = QtWidgets.QVBoxLayout()
        open_button_layout.setAlignment(Qt.AlignCenter)
        open_button_layout.addStretch()
        open_button = QtWidgets.QPushButton("Open")
        open_button.setFixedSize(200, 75)
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

    def open_action(self):
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget() is not None:
                item.widget().deleteLater()
            elif item.layout() is not None:
                item.layout().deleteLater()
        self.content_layout.addWidget(TableWidget())


class TableWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Table Widget")

        # create main horizontal layout
        main_layout = QtWidgets.QHBoxLayout()

        # create table
        table = QtWidgets.QTableWidget()
        table.setColumnCount(2)
        table.setRowCount(2)
        table.setHorizontalHeaderLabels(["User", "VAS"])
        table.setVerticalHeaderLabels(["User", "VAS"])

        # add play buttons to table
        play_button1 = QtWidgets.QPushButton("Play")
        play_button2 = QtWidgets.QPushButton("Play")
        table.setCellWidget(0, 1, play_button1)
        table.setCellWidget(1, 1, play_button2)

        # add table to main layout and add scrollbar
        main_layout.addWidget(table)
        scrollbar = QtWidgets.QScrollBar()
        main_layout.addWidget(scrollbar)

        # set main layout
        self.setLayout(main_layout)


