import sys
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget

class WorkerThread(QThread):
    finished_signal = pyqtSignal()

    def run(self):
        # Simulate some time-consuming work
        self.msleep(3000)
        self.finished_signal.emit()

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Thread Termination Example")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.terminate_button = QPushButton("Terminate Application", self)
        self.terminate_button.clicked.connect(self.create_thread)
        layout.addWidget(self.terminate_button)

        self.worker_thread = None

    def create_thread(self):
        if self.worker_thread is None or not self.worker_thread.isRunning():
            self.worker_thread = WorkerThread()
            self.worker_thread.finished_signal.connect(self.terminate_application)
            self.worker_thread.start()

    def terminate_application(self):
        print("Thread finished. Terminating application.")
        app.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MyMainWindow()
    main_window.show()

    sys.exit(app.exec())
