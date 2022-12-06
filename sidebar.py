from PyQt5 import QtWidgets, QtCore

from visualization import VisualizationWidget


class SidebarWidget(QtWidgets.QWidget):
    def __init__(self, main_content_widget):
        super().__init__()

        self.main_content_widget = main_content_widget
        self.downloading_widget = self.main_content_widget.old_widget
        self.visualization_widget = VisualizationWidget()

        # Create a vertical layout for the sidebar
        self.sidebar_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.sidebar_layout)

        # Add a vertical layout to the sidebar for the buttons
        self.sidebar_button_layout = QtWidgets.QVBoxLayout()
        self.sidebar_layout.addLayout(self.sidebar_button_layout)

        # Set the alignment of the buttons to top-aligned
        self.sidebar_button_layout.setAlignment(QtCore.Qt.AlignTop)

        def to_downloading():
            self.main_content_widget.set_widget(self.downloading_widget)

        def to_visualization():
            self.main_content_widget.set_widget(self.visualization_widget)

        # Create three buttons and add them to the sidebar button layout
        self.button_downloading = QtWidgets.QPushButton("Downloading")
        self.button_downloading.clicked.connect(to_downloading)
        self.sidebar_button_layout.addWidget(self.button_downloading)
        self.button_visualization = QtWidgets.QPushButton("Visualization")
        self.button_visualization.clicked.connect(to_visualization)
        self.sidebar_button_layout.addWidget(self.button_visualization)
        self.button_labeling = QtWidgets.QPushButton("Labeling")
        self.sidebar_button_layout.addWidget(self.button_labeling)

        # Add some styling to the buttons
        self.button_downloading.setStyleSheet("background-color: #7acfff; color: white; font-size: 14pt; padding: 10px")
        self.button_visualization.setStyleSheet("background-color: #7acfff; color: white; font-size: 14pt; padding: 10px")
        self.button_labeling.setStyleSheet("background-color: #7acfff; color: white; font-size: 14pt; padding: 10px")


