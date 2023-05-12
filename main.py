from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QApplication

from downloading import DownloadingWidget
from sidebar import SidebarWidget


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Set window properties
        self.setWindowTitle("VAS Tool Box")
        self.setMinimumSize(850, 600)

        # Create a widget for the main content area
        self.main_widget = QtWidgets.QWidget()
        # self.main_widget.setStyleSheet("background-color: grey")
        self.setCentralWidget(self.main_widget)

        # Create a vertical layout for the main content area
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        # Create a horizontal splitter for the main content area
        self.splitter = QtWidgets.QSplitter()
        self.main_layout.addWidget(self.splitter)

        # Create a widget for the sidebar and add it to the splitter
        self.main_content_widget = MainContentWidget(DownloadingWidget())
        self.sidebar_widget = SidebarWidget(self.main_content_widget)
        self.splitter.addWidget(self.sidebar_widget)

        # Make the size of the sidebar changeable
        self.splitter.setSizes([150, 450])

        # Create a widget for the main content and add it to the splitter
        self.splitter.addWidget(self.main_content_widget)


class MainContentWidget(QtWidgets.QWidget):
    def __init__(self, widget):
        super().__init__()
        self.main_layout = QtWidgets.QVBoxLayout()
        self.old_widget = widget
        self.main_layout.addWidget(widget)
        self.setLayout(self.main_layout)

    def set_widget(self, widget):
        self.old_widget.setParent(None)
        self.old_widget = widget
        self.main_layout.addWidget(self.old_widget)


if __name__ == '__main__':
    # QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)  # enable highdpi scaling
    # QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)  # use highdpi icons
    app = QApplication([])
    window = MainWindow()
    window.show()
    with open("style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)
    app.exec()
