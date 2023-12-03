from test_design import Ui_MainWindow
from PyQt6 import QtCore, QtGui, QtWidgets
from tools.functionality import Functionality
from tools.functionality import SEARCH_BUSINESS_FILTER, SEARCH_BUSINESS_ORDER, SEARCH_USER_YELP
import pypyodbc
from dotenv import dotenv_values
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QDialog, QProgressDialog
from PyQt6.QtCore import Qt, QTimer

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QTimer

class LoadingScreen(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("Loading Screen")
        self.setGeometry(100, 100, 400, 200)

        # Create a central widget and set it as the main window's central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a vertical layout for the central widget
        layout = QVBoxLayout(central_widget)

        # Add a label for the loading message
        self.loading_label = QLabel("Loading...", self)
        layout.addWidget(self.loading_label)

        # Create a timer to simulate loading (you can replace this with your actual loading logic)
        self.loading_timer = QTimer(self)
        self.loading_timer.timeout.connect(self.update_loading_message)
        self.loading_timer.start(500)  # Update every 500 milliseconds

    def update_loading_message(self):
        # Update the loading message
        current_text = self.loading_label.text()
        dots = current_text.count('.')
        dots = (dots + 1) % 4
        self.loading_label.setText("Loading" + "." * dots)


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
    controller.setCursor(controller.init_connection(
        db_host=db_host,
        db_name=db_name,
        db_password=db_password,
        db_user=db_user
    ))
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