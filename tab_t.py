import sys

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QVBoxLayout, QPushButton


class MainWindow(QWidget):
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

        # Add a few tabs
        for i in range(3):
            self.tabs.addTab(QWidget(), "Tab {}".format(i))

    def close_tab(self, index):
        # Get the widget for the tab
        widget = self.tabs.widget(index)

        # Remove the widget and the tab
        widget.deleteLater()
        self.tabs.removeTab(index)

    def add_tab(self):
        # Add a new tab with a default name
        self.tabs.addTab(QWidget(), "New Tab")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
