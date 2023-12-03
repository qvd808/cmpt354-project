from test_design import Ui_MainWindow
from PyQt6 import QtWidgets
from tools.functionality import Functionality
from tools.functionality import SEARCH_BUSINESS_FILTER, SEARCH_BUSINESS_ORDER, SEARCH_USER_YELP
import pypyodbc
from dotenv import dotenv_values
from PyQt6.QtCore import Qt, QThread, pyqtSignal

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


class Application(Ui_MainWindow):
    def __init__(self, Window: QtWidgets.QMainWindow, controller: Functionality, db_host, db_name, db_user, db_password) -> None:
        super().__init__()

        self.setupUi(Window)
        self.controller = controller

        # try:
        #     self.connec_database()
        # except pypyodbc.Error as e:
        #     print(e)
        # try:
        #     self.controller.setCursor(self.controller.init_connection(
        #         db_host=db_host,
        #         db_name=db_name,
        #         db_password=db_password,
        #         db_user=db_user
        #     ))
        # except pypyodbc.DatabaseError:
        #     print("Unable to connect")
        self.pushButton.clicked.connect(self.sign_in_function)
        self.worker_thread = None
        self.run_on_startup()

    def run_on_startup(self):
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

    def connec_database(self):
            self.controller.setCursor(self.controller.init_connection(
                db_host=db_host,
                db_name=db_name,
                db_password=db_password,
                db_user=db_user
            ))


    def sign_in_function(self):
        print("Hello world")


if __name__ == "__main__":
    import sys
    from dotenv import dotenv_values



    config = dotenv_values(".env")  # take environment variables from .env.

    db_host = config['DB_HOST']
    db_name = config['DB_NAME']
    db_user = config['DB_USER']
    db_password = config['DB_PASSWORD']

    app = QtWidgets.QApplication(sys.argv)
    controller = Functionality()

    MainWindow = QtWidgets.QMainWindow()
    ui = Application(
        MainWindow,
        controller=controller,
        db_name=db_name,
        db_host=db_host,
        db_password=db_password,
        db_user=db_user
    )
    MainWindow.show()
    app.exec()