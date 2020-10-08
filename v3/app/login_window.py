import sys
import requests
import json

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QListView
from PyQt5.QtWidgets import QMessageBox, QListWidget, QLabel, QLineEdit

from app_window import AppWindow


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Login"
        self.width = 800
        self.height = 600
        self.URL = "http://localhost:8000"

        self.username = None
        self.password = None

        self.initialize()

    def initialize(self):
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)
        self.get_username()
        self.get_password()

        login_bt = QPushButton("Login", self)
        login_bt.move(460, 200)
        login_bt.clicked.connect(self.login)

        self.show()

    def get_username(self):
        username_label = QLabel(self)
        username_label.setText("Username: ")
        username_label.move(420, 120)

        self.username = QLineEdit(self)
        self.username.move(500, 120)
    
    def get_password(self):
        password_label = QLabel(self)
        password_label.setText("Password: ")
        password_label.move(420, 160)

        self.password = QLineEdit(self)
        self.password.move(500, 160)
    
    def login(self):
        if not self.password.text() or not self.username.text():
            QMessageBox.about(self, "Error", "\nPlease fill all entries\t\n")
        else:
            login_stats = requests.get(self.URL+'/login?username='+
                                       self.username.text()+
                                       '&password='+self.password.text())
            login_stats = json.loads(login_stats.text)
            if login_stats['status'] == True:
                self.app_window = AppWindow(user=self.username.text())
            else:
                QMessageBox.about(self, "Login Failed", "\nPlease try again\t\n")

        

App = QApplication(sys.argv)
w = LoginWindow()
sys.exit(App.exec())
