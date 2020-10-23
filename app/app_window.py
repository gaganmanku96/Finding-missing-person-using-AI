import sys
import requests
import json
import base64
import io

from PIL import Image
import numpy as np
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QListView, QBoxLayout
from PyQt5.QtWidgets import QMessageBox, QListWidget, QLabel, QLineEdit

from new_case import NewCase
from train_model import train
from match_faces import match


class AppWindow(QMainWindow):
    def __init__(self, user):
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

        confirmedButton = QPushButton("Confirmed", self)
        confirmedButton.move(470, 250)
        confirmedButton.clicked.connect(self.view_confirmed_cases)

        self.show()
        
    def new_case(self):
        self.new_case = NewCase(self.user)

    def refresh_model(self):
        output = train(self.user)
        if output['status']:
            QMessageBox.about(self, "Success", output['message'])
        else:
            QMessageBox.about(self, "Error", output['message'])

    def match_from_submitted(self):
        output = match()
        if output['status']:
            result = output['result']
            self.view_cases(result)
        else:
            QMessageBox.about(self, "Error", output['message'])

    def view_confirmed_cases(self):
        # self.view_cases()
        pass

    def view_cases(self, result):
        list_ = QListView(self)
        list_.setIconSize(QSize(96, 96))
        list_.setMinimumSize(400, 380)
        list_.move(40, 40)
        model = QStandardItemModel(list_)
        item = QStandardItem("Matched")
        model.appendRow(item)

        for case_id, submission_list in result.items():
            case_details = self.get_details(case_id, "case")
            for submission_id in submission_list:
                submission_details = self.get_details(submission_id, "user")
                image = self.decode_base64(case_details[0][2])

                item = QStandardItem(
                        " Name: " + case_details[0][0] +
                        "\n Father's Name: " + case_details[0][1] +
                        "\n Age: " + str(case_details[0][4]) +
                        "\n Mobile " + str(case_details[0][3]) +
                        "\n Location " + submission_details[0][0]
                        # "\n Matched Date" + submission_details[0][1]
                        )
                image = QtGui.QImage(image,
                                     image.shape[1],
                                     image.shape[0],
                                     image.shape[1] * 3,
                                     QtGui.QImage.Format_RGB888)
                icon = QPixmap(image)
                item.setIcon(QIcon(icon))
                model.appendRow(item)

        list_.setModel(model)
        list_.show()
    
    def get_details(self, case_id: str, type: str):
        if type == 'user':
            URL = f"http://localhost:8000/get_user_details?case_id='{case_id}'"
        else:
            URL = f"http://localhost:8000/get_case_details?case_id='{case_id}'"
        try:
            result = requests.get(URL)
            if result.status_code == 200:
                return json.loads(result.text)
            else:
                pass
        except Exception as e:
            raise e
    
    def decode_base64(self, img: str):
        """
        Image is converted ot numpy array.
        """
        img = np.array(Image.open(io.BytesIO(base64.b64decode(img))))
        return img
