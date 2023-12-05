from test_login_screen import Ui_LoginScreen
from PyQt6 import QtWidgets, QtCore
from tools.functionality import Functionality
from tools.functionality import SEARCH_BUSINESS_FILTER, SEARCH_BUSINESS_ORDER, SEARCH_USER_YELP
import pypyodbc, sys
from dotenv import dotenv_values
from PyQt6.QtCore import QThread, pyqtSignal, QRect
from PyQt6.QtWidgets import QMessageBox, QProgressBar,QVBoxLayout, QDialog, QWidget,QTableWidget, QTableWidgetItem,QHeaderView
from PyQt6.QtWidgets import QStyledItemDelegate, QComboBox, QMenu
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
        self.pushButton_2.clicked.connect(self.backtoSearch)
        self.table = QTableWidget(self)
        self.table.hide()

    def backtoSearch(self):
        widget.setCurrentWidget(search_screen)

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
                self.textEdit.setText("")
                self.textEdit.setPlaceholderText("Please enter a number")
            case "City":    
                self.current_filter = "CITY"
                self.textEdit.setText("")
                self.textEdit.setPlaceholderText("Please enter a city")
            case "Name":    
                self.current_filter = "NAME"
                self.textEdit.setText("")
                self.textEdit.setPlaceholderText("Please enter a name")

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
                message="Please set the Filter for search business",
                title="Missing Filter options"
            )
            return
        if self.current_order == None:
            self.show_message(
                message="Please set the Order for search business",
                title="Missing Sort By options"
            )
            return
        
        filter = SEARCH_BUSINESS_FILTER(variant=self.current_filter, value=self.textEdit.toPlainText())
        order = SEARCH_BUSINESS_ORDER(variant=self.current_order)
        row = controller.search_business(filter=filter, orders=order)
        self.createLabel(row)
    
    def createLabel(self, row):
        self.table.setRowCount(len(row))
        self.table.setColumnCount(len(row[0]) + 1)
        self.table.setGeometry(QRect(35, 231, 1031, 511))
        self.table.setHorizontalHeaderLabels((
            "Business Id",
            "Name",
            "Address",
            "City",
            "Number of stars",
            "Review business"
        ))
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)

        for (col, item) in enumerate(row):
            for (row, value) in enumerate(item):
                self.table.setItem(col, row, QTableWidgetItem(str(value)))
        self.table.show()

    def contextMenuEvent(self, event):
        selected_indexes = self.table.selectedIndexes()
        if not selected_indexes:
            return
        for index in selected_indexes:
            row = index.row()
            self.table.selectRow(row)

        menu = QMenu(self)
        action = menu.addAction("Review Business")
        action.triggered.connect(self.executeFunction)
        menu.exec(event.globalPos())

    def executeFunction(self, row):
        selected_indexes = self.table.selectedIndexes()
        for index in selected_indexes:
            row = index.row()
            column = index.column()
            if column != 0:
                return
            self.reviewBusiness(self.table.item(row, 0).text())

    def reviewBusiness(self, business_id):
        from PyQt6.QtWidgets import QInputDialog
        dialog = QInputDialog()
        dialog.setLabelText("Enter your rating")
        result = dialog.exec()
        if result:
            value = dialog.textValue()
            try:
                if 1 <= int(value) <= 5:
                    controller.review_business(ui.current_user, business_id, value)
                else:
                    error_message = QMessageBox()
                    error_message.setWindowTitle("Invalid input")
                    error_message.setText("Please enter integer from 1 to 5")
                    error_message.exec()     
            except ValueError:
                error_message = QMessageBox()
                error_message.setWindowTitle("Invalid input")
                error_message.setText("Please enter integer from 1 to 5")
                error_message.exec()     
        else:
            # User pressed Cancel, handle it as needed (e.g., return a default value or raise an exception)
            print("Cancle")
            return None
    

class SearchUserScreen(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("./screens/search_user.ui", self)
        self.current_filter = None
        self.comboBox.currentTextChanged.connect(self.setFilter)

        self.pushButton.clicked.connect(self.search_business)
        self.pushButton_2.clicked.connect(self.backtoSearch)
        self.table = QTableWidget(self)
        self.table.hide()

    def backtoSearch(self):
        widget.setCurrentWidget(search_screen)

    def setFilter(self, text):
        match text:
            case "Minimum review count":    
                self.current_filter = "MIN_REVIEW_COUNT"
                self.textEdit.setText("")
                self.textEdit.setPlaceholderText("Please enter a number")
            case "Minimum average stars":    
                self.current_filter = "MIN_AVG_STAR"
                self.textEdit.setText("")
                self.textEdit.setPlaceholderText("Please enter a number")
            case "Name":    
                self.current_filter = "NAME"
                self.textEdit.setText("")
                self.textEdit.setPlaceholderText("Please enter a number")
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
                message="Please set the Filter for search business",
                title="Missing Filter options"
            )
            return
        
        filter = SEARCH_USER_YELP(variant=self.current_filter, value=self.textEdit.toPlainText())
        row = controller.search_users(filter=filter)
        self.createLabel(row)
    
    def createLabel(self, row):
        self.table.setRowCount(len(row))
        self.table.setColumnCount(len(row[0]))
        self.table.setGeometry(QRect(35, 231, 1031, 511))
        self.table.setHorizontalHeaderLabels((
            "User Id",
            "Name",
            "Review count",
            "Useful",
            "Funny",
            "Cool",
            "Avg. stars",
            "Date created"
        ))
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)

        for (col, item) in enumerate(row):
            for (row, value) in enumerate(item):
                self.table.setItem(col, row, QTableWidgetItem(str(value)))
        self.table.show()

    def contextMenuEvent(self, event):
        selected_indexes = self.table.selectedIndexes()
        if not selected_indexes:
            return
        for index in selected_indexes:
            row = index.row()
            self.table.selectRow(row)

        menu = QMenu(self)
        action = menu.addAction("Add Friend")
        action.triggered.connect(self.executeFunction)
        menu.exec(event.globalPos())

    def executeFunction(self, row):
        selected_indexes = self.table.selectedIndexes()
        for index in selected_indexes:
            row = index.row()
            column = index.column()
            if column != 0:
                return
            self.AddFriend(self.table.item(row, 0).text())
    def AddFriend(self, row):
        if controller.make_friend(ui.current_user, row):
            self.show_message(f"Successfully adding {ui.current_user} as your friend", "Success")
        else:
            self.show_message(f"{ui.current_user} is already your friend", "Failed")
            

class SearchScreen(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("./screens/search_screen.ui", self)
        self.pushButton.clicked.connect(self.goToSearchBusinnesses)
        self.pushButton_2.clicked.connect(self.goToSearchUsers)
        self.pushButton_3.clicked.connect(self.backToLogin)
    
    def backToLogin(self):
        widget.setCurrentWidget(ui.centralwidget)
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

        db_host="cypress.csil.sfu.ca"
        db_name = "qvd354"
        db_user = "s_qvd"
        db_password = "Ttmq6yAbH4FAnFgJ"
        try:

            if sys.platform == 'darwin':
                connection_string = 'Driver={ODBC Driver 17 for SQL Server};Server=' + db_host + ';Database=' + db_name + ';UID=' + db_user + ';PWD=' + db_password + ';'
            else:
                connection_string = 'Driver={SQL Server};Server=' + db_host + ';Database=' + db_name + ';UID=' + db_user + ';PWD=' + db_password + ';'

            connection = pypyodbc.connect(connection_string)
            self.setCusor(connection.cursor())
            controller.setConnection(connection)
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
        self.setGeometry(1050, 300, 550, 100)
        self.setWindowTitle('Connecting to qvd354 database')
        self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)
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
    def __init__(self, Window: QtWidgets.QMainWindow, controller: Functionality) -> None:
        super().__init__()

        self.popup = PopupQProgressDialog(controller.setCursor, self)
        self.setupUi(Window)
        self.controller = controller
        self.pushButton.clicked.connect(self.sign_in_function)
        self.current_user = None

        self.screens = QtWidgets.QStackedWidget()


    def show_message(self, message, title):
        message_box = QMessageBox()
        message_box.setWindowTitle(title)
        message_box.setText(message)
        message_box.exec()

    def sign_in_function(self):
        user_id = self.textEdit.toPlainText()
        if self.controller.login(user_id):
            self.current_user = user_id
            self.textEdit.setText("")
            print("Login successfully")
            widget.setCurrentWidget(search_screen)

        else:
            self.textEdit.setText("")
            message_box = QMessageBox()
            import random
            chance = random.randint(1, 5)
            if chance == 1:
                self.label.setText("Is this a valid User ID?")
                self.label.setStyleSheet("color: #F00;\n"
                "text-align: center;\n"
                "font-family: Inter;\n"
                "font-size: 64px;\n"
                "font-style: normal;\n"
                "font-weight: 400;\n"
                "line-height: normal;")
            else:
                self.label.setText("Please enter your User ID")
                self.label.setStyleSheet("color: #6D6F11;\n"
                "text-align: center;\n"
                "font-family: Inter;\n"
                "font-size: 64px;\n"
                "font-style: normal;\n"
                "font-weight: 400;\n"
                "line-height: normal;")    

            message_box.setWindowTitle('Invalid User ID!!')
            message_box.setText('The User Id you enter is invalid, please enter a different User ID')
            message_box.exec()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    controller = Functionality()

    #initialize the app and screen
    MainWindow = QtWidgets.QMainWindow()
    widget = QtWidgets.QStackedWidget()
    ui = Application(
        MainWindow,
        controller=controller
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