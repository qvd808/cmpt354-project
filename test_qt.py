from test_design import Ui_MainWindow
from PyQt6 import QtWidgets
from tools.functionality import Functionality
from tools.functionality import SEARCH_BUSINESS_FILTER, SEARCH_BUSINESS_ORDER, SEARCH_USER_YELP
import pypyodbc
from dotenv import dotenv_values
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import QProgressDialog, QMessageBox, QProgressBar,QVBoxLayout,QLabel, QWidget

class WorkerThread(QThread):
    finished_signal = pyqtSignal(bool)

    def __init__(self, setCursor, parent = None):
        QThread.__init__(self, parent)
        self.setCusor = setCursor

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
            self.setCusor(connection.cursor())
            self.finished_signal.emit(True)
        except Exception as e:
            self.finished_signal.emit(False)


class PopupQProgressDialog(QWidget):
    def __init__(self, setCursor, main_app):
        super().__init__()
        self.bar = QProgressBar(self)
        self.bar.setGeometry(30,40,500, 75)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.bar)
        self.setLayout(self.layout)
        self.setGeometry(300, 300, 550, 100)
        self.setWindowTitle('Progress Bar')
        self.bar.setRange(0, 0)
        self.worker_thread = None
        self.main_app = main_app
        self.setCursor = setCursor

        if self.worker_thread is None or not self.worker_thread.isRunning():
            self.worker_thread = WorkerThread(self.setCursor)
            self.worker_thread.finished_signal.connect(self.handle_thread_result)
            self.show()
            self.worker_thread.start()  
        
    def handle_thread_result(self, connection_successful):
        if connection_successful:
            print("Connection successful.")
            message_box = QMessageBox()
            message_box.setWindowTitle('Database connection successful!!')
            message_box.setText('Connected to database of qvd354!')
            message_box.exec()
            self.close()
        else:
            print("Connection failed. Terminating application.")
            message_box = QMessageBox()
            message_box.setWindowTitle('Database connection failed!!')
            message_box.setText('Can not connect to the database, please make sure that you are connected to the SFU net work on your computer is connecting to the internet!')
            message_box.exec()
            sys.exit()

class Application(Ui_MainWindow):
    def __init__(self, Window: QtWidgets.QMainWindow, controller: Functionality, db_host, db_name, db_user, db_password) -> None:
        super().__init__()

        self.setupUi(Window)
        self.controller = controller
        self.popup = PopupQProgressDialog(controller.setCursor, self)
        self.pushButton.clicked.connect(self.sign_in_function)

    def connec_database(self):
            self.controller.setCursor(self.controller.init_connection(
                db_host=db_host,
                db_name=db_name,
                db_password=db_password,
                db_user=db_user
            ))


    def sign_in_function(self):
        user_id = self.textEdit.toPlainText()
        if self.controller.login(user_id):
            print("Login successfully")
        else:
            self.textEdit.setText("")
            message_box = QMessageBox()
            message_box.setWindowTitle('Invalid User ID!!')
            message_box.setText('The User Id you enter is invalid, please enter a different User ID')
            message_box.exec()


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