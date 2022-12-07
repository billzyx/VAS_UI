import time
from PyQt5 import QtCore, QtWidgets


class MyWorker(QtCore.QObject):
    # Signal that will be emitted during the process
    update_progress = QtCore.pyqtSignal(int)
    finished = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    @QtCore.pyqtSlot()
    def run(self):
        # This is the code that will run in the new thread
        total = 100
        for i in range(total):
            time.sleep(0.1)  # Simulate some work
            self.update_progress.emit(i + 1)
        # Emit a signal that the process is finished
        self.finished.emit()


class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.worker = MyWorker()  # Create the worker

        # Set up the progress bar
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setRange(0, 100)

        # Connect the signal from the worker to the progress bar
        self.worker.update_progress.connect(self.progress_bar.setValue)

        # Connect the finished signal to a slot
        self.worker.finished.connect(self.on_finished)

        # Create a button to start the worker
        self.start_button = QtWidgets.QPushButton("Start")
        self.start_button.clicked.connect(self.start)

        # Create a layout and add the widgets
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.start_button)
        self.setLayout(layout)

    def start(self):
        self.start_button.setEnabled(False)  # Disable the start button
        self.thread = QtCore.QThread()  # Create a new thread
        self.worker.moveToThread(self.thread)  # Move the worker to the new thread
        self.thread.started.connect(self.worker.run)  # Start the worker when the thread starts
        self.thread.start()  # Start the thread

    @QtCore.pyqtSlot()
    def on_finished(self):
        self.start_button.setEnabled(True)  # Enable the start button
        self.start_button.setText("Finished")  # Change the text of the button


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()
