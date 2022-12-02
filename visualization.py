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