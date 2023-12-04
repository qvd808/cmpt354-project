# Form implementation generated from reading ui file 'screens/search_business.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1093, 774)
        self.textEdit = QtWidgets.QTextEdit(parent=Form)
        self.textEdit.setGeometry(QtCore.QRect(50, 80, 661, 41))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.textEdit.setFont(font)
        self.textEdit.setStyleSheet("border-radius: 30px;\n"
"border: 3px solid #AAA;\n"
"background: #D9D9D9;")
        self.textEdit.setObjectName("textEdit")
        self.pushButton = QtWidgets.QPushButton(parent=Form)
        self.pushButton.setGeometry(QtCore.QRect(230, 150, 251, 61))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("border-radius: 30px;\n"
"border: 2px solid #665720;\n"
"background: #AC9956;")
        self.pushButton.setObjectName("pushButton")
        self.comboBox = QtWidgets.QComboBox(parent=Form)
        self.comboBox.setGeometry(QtCore.QRect(740, 70, 151, 51))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.comboBox.setFont(font)
        self.comboBox.setStyleSheet("border-radius: 30px;\n"
"border: 3px solid #AAA;\n"
"background: #D9D9D9;")
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox_3 = QtWidgets.QComboBox(parent=Form)
        self.comboBox_3.setGeometry(QtCore.QRect(920, 70, 141, 51))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.comboBox_3.setFont(font)
        self.comboBox_3.setStyleSheet("border-radius: 30px;\n"
"border: 3px solid #AAA;\n"
"background: #D9D9D9;")
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.pushButton_2 = QtWidgets.QPushButton(parent=Form)
        self.pushButton_2.setGeometry(QtCore.QRect(560, 150, 251, 61))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("border-radius: 30px;\n"
"border: 2px solid #665720;\n"
"background: #AC9956;")
        self.pushButton_2.setObjectName("pushButton_2")
        self.progressBar = QtWidgets.QProgressBar(parent=Form)
        self.progressBar.setGeometry(QtCore.QRect(220, 280, 611, 51))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.textEdit.setPlaceholderText(_translate("Form", "Enter a restaurant name"))
        self.pushButton.setText(_translate("Form", "Search"))
        self.comboBox.setItemText(0, _translate("Form", "Filter By"))
        self.comboBox.setItemText(1, _translate("Form", "Minimum number of stars"))
        self.comboBox.setItemText(2, _translate("Form", "City"))
        self.comboBox.setItemText(3, _translate("Form", "Name"))
        self.comboBox_3.setItemText(0, _translate("Form", "Sort By"))
        self.comboBox_3.setItemText(1, _translate("Form", "Name"))
        self.comboBox_3.setItemText(2, _translate("Form", "City"))
        self.comboBox_3.setItemText(3, _translate("Form", "Number of stars"))
        self.pushButton_2.setText(_translate("Form", "Back"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())