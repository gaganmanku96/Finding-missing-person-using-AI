import sys

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QListView
from PyQt5.QtWidgets import QMessageBox, QListWidget, QLabel, QLineEdit

from new_case import NewCase
from train_model import train


class AppWindow(QMainWindow):
    def __init__(self, user="admin"):
        super().__init__()
        self.title = "Application"
        self.width = 800
        self.height = 600
        self.user = user

        self.initialize()

    def initialize(self):
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)

        button_upload = QPushButton("New Case", self)
        button_upload.move(470, 100)
        button_upload.clicked.connect(self.new_case)

        button_refresh_model = QPushButton("Refresh", self)
        button_refresh_model.move(470, 150)
        button_refresh_model.clicked.connect(self.refresh_model)

        button_match = QPushButton("Match", self)
        button_match.move(470, 200)
        button_match.clicked.connect(self.match_from_submitted)

        confirmedButton = QPushButton("Confirmed cases", self)
        confirmedButton.move(470, 250)
        confirmedButton.clicked.connect(self.view_confirmed_cases)

        self.show()
        
    def new_case(self):
        self.new_case = NewCase()

    def refresh_model(self):
        output = train(self.user)
        if output['status']:
            QMessageBox.about(self, "Success", output['message'])
        else:
            QMessageBox.about(self, "Error", output['message'])

    def match_from_submitted(self):
        pass

    def view_confirmed_cases(self):
        pass


App = QApplication(sys.argv)
w = AppWindow()
sys.exit(App.exec())