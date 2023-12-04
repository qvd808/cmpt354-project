from test_login_screen import Ui_LoginScreen
from PyQt6 import QtWidgets, QtCore
from tools.functionality import Functionality
from tools.functionality import SEARCH_BUSINESS_FILTER, SEARCH_BUSINESS_ORDER, SEARCH_USER_YELP
import pypyodbc
from dotenv import dotenv_values
from PyQt6.QtCore import QThread, pyqtSignal, QRect
from PyQt6.QtWidgets import QMessageBox, QProgressBar,QVBoxLayout, QDialog, QWidget,QTableWidget, QTableWidgetItem,QHeaderView
from PyQt6.uic import loadUi

class SearchBusinessScreen(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("./screens/search_business.ui", self)
        self.current_filter = None
        self.current_order = None
        self.comboBox.currentTextChanged.connect(self.setFilter)
        self.comboBox_3.currentTextChanged.connect(self.setOrder)

        self.pushButton.clicked.connect(self.search_business)
        self.table = QTableWidget(self)
        self.table.hide()

    def setOrder(self, text):
        match text:
            case "Number of stars":    
                self.current_order = "NO_OF_STARS"
            case "City":    
                self.current_order = "CITY"
            case "Name":    
                self.current_order = "NAME"
            case _:
                self.current_filter = None

    def setFilter(self, text):
        match text:
            case "Minimum number of stars":    
                self.current_filter = "MIN_STAR"
            case "City":    
                self.current_filter = "CITY"
            case "Name":    
                self.current_filter = "NAME"
            case _:
                self.current_filter = None

    def show_message(self, message, title):
        message_box = QMessageBox()
        message_box.setWindowTitle(title)
        message_box.setText(message)
        message_box.exec()

    def search_business(self):
        if self.current_filter == None:
            self.show_message(
                message="Please set the Filter for search business"
            )
            return
        if self.current_order == None:
            self.show_message(
                message="Please set the Order for search business"
            )
            return
        
        filter = SEARCH_BUSINESS_FILTER(variant=self.current_filter, value=self.textEdit.toPlainText())
        order = SEARCH_BUSINESS_ORDER(variant=self.current_order)
        row = controller.search_business(filter=filter, orders=order)
        self.createLabel(row)
    
    def createLabel(self, row):
        self.table.setRowCount(len(row))
        self.table.setColumnCount(len(row[0]))
        self.table.setGeometry(QRect(35, 231, 1031, 511))
        self.table.setHorizontalHeaderLabels((
            "Business Id",
            "Name",
            "Address",
            "City",
            "Number of stars"
        ))
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)

        for (col, item) in enumerate(row):
            for (row, value) in enumerate(item):
                self.table.setItem(col, row, QTableWidgetItem(str(value)))
        self.table.show()
        # self.addWidget(self.table)

class SearchUserScreen(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("./screens/search_user.ui", self)


class SearchScreen(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("./screens/search_screen.ui", self)
        self.pushButton.clicked.connect(self.goToSearchBusinnesses)
        self.pushButton_2.clicked.connect(self.goToSearchUsers)
    
    def goToSearchBusinnesses(self):
        widget.setCurrentWidget(search_business_screen)
    def goToSearchUsers(self):
        widget.setCurrentWidget(search_user_screen)

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
            self.main_app.show_message(
                message = 'Connected to database of qvd354!',
                title='Database connection successful!!'
            )
            self.close()
        else:
            print("Connection failed. Terminating application.")
            self.main_app.show_message(
                message = 'Can not connect to the database, please make sure that you are connected to the SFU net work on your computer is connecting to the internet!',
                title='Database connection failed!!'
            )
            sys.exit()

class Application(Ui_LoginScreen):
    def __init__(self, Window: QtWidgets.QMainWindow, controller: Functionality, db_host, db_name, db_user, db_password) -> None:
        super().__init__()

        self.setupUi(Window)
        self.controller = controller
        self.popup = PopupQProgressDialog(controller.setCursor, self)
        self.pushButton.clicked.connect(self.sign_in_function)

        self.screens = QtWidgets.QStackedWidget()


    def show_message(self, message, title):
        message_box = QMessageBox()
        message_box.setWindowTitle(title)
        message_box.setText(message)
        message_box.exec()

    def sign_in_function(self):
        user_id = self.textEdit.toPlainText()
        if self.controller.login(user_id):
            print("Login successfully")
            widget.setCurrentWidget(search_screen)
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

#initialize the app and screen
    MainWindow = QtWidgets.QMainWindow()
    widget = QtWidgets.QStackedWidget()
    ui = Application(
        MainWindow,
        controller=controller,
        db_name=db_name,
        db_host=db_host,
        db_password=db_password,
        db_user=db_user
    )
    search_screen = SearchScreen()
    search_business_screen = SearchBusinessScreen()
    search_user_screen = SearchUserScreen()
    widget.addWidget(ui.centralwidget)
    widget.addWidget(search_screen)
    widget.addWidget(search_business_screen)
    widget.addWidget(search_user_screen)
    widget.resize(1092, 774)
    widget.setCurrentWidget(ui.centralwidget)
    widget.show()

    app.exec()