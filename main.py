import sys
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QLabel
import pypyodbc

class WorkerThread(QThread):
    finished_signal = pyqtSignal(bool)

    def run(self):
        # Simulate some time-consuming work
        from dotenv import dotenv_values
        config = dotenv_values(".env")  # take environment variables from .env.

        db_host = config['DB_HOST']
        db_name = config['DB_NAME']
        db_user = config['DB_USER']
        db_password = config['DB_PASSWORD']
        try:
            connection_string = 'Driver={SQL Server};Server=' + db_host + ';Database=' + db_name + ';UID=' + db_user + ';PWD=' + db_password + ';'
            connection = pypyodbc.connect(connection_string)
            self.finished_signal.emit(True)
        except Exception as e:
            self.finished_signal.emit(False)

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

        self.result_label = QLabel(self)
        layout.addWidget(self.result_label)

        self.worker_thread = None

    def create_thread(self):
        if self.worker_thread is None or not self.worker_thread.isRunning():
            self.worker_thread = WorkerThread()
            self.worker_thread.finished_signal.connect(self.handle_thread_result)
            self.worker_thread.start()

    def handle_thread_result(self, connection_successful):
        if connection_successful:
            print("Connection successful.")
            self.terminate_button.hide()
            self.result_label.setText("Connection successful.")
        else:
            print("Connection failed. Terminating application.")
            app.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MyMainWindow()
    main_window.show()

    sys.exit(app.exec())