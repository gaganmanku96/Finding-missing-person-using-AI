import os
import shutil
import subprocess
import time
import base64
import io

import cv2
from PIL import Image
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QPushButton
from PyQt5.QtWidgets import QInputDialog, QLabel, QLineEdit, QMessageBox

import face_encoding
import db_operations


class NewCase(QMainWindow):
    def __init__(self, parent=None):
        super().__init__().__init__(parent)

        self.title = "Register New Case"
        self.name = ""
        self.age = ""
        self.mob = ""
        self.father_name = ""
        self.image = None
        self.encoded_image = None
        self.key_points = None
        self.initialize()

    def initialize(self):
        self.setFixedSize(600, 400)
        self.setWindowTitle(self.title)

        uploadImageBT = QPushButton("select image file", self)
        uploadImageBT.move(400, 20)
        uploadImageBT.clicked.connect(self.openFileNameDialog)

        saveBT = QPushButton("Save ", self)
        saveBT.move(400, 350)
        saveBT.clicked.connect(self.save)

        self.getName()
        self.getAge()
        self.getFName()
        self.getMob()
        self.show()

    def getName(self):
        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Name:')
        self.lineName = QLineEdit(self)
        self.lineName.move(480, 70)
        self.nameLabel.move(420, 70)
        # self.line.resize(200, 32)

    def getAge(self):
        self.ageLabel = QLabel(self)
        self.ageLabel.setText('Age:')
        self.lineAge = QLineEdit(self)
        self.lineAge.move(480, 110)
        self.ageLabel.move(420, 110)

    def getFName(self):
        self.FnameLabel = QLabel(self)
        self.FnameLabel.setText('Father\'s\n Name:')
        self.lineFName = QLineEdit(self)
        self.lineFName.move(480, 150)
        self.FnameLabel.move(420, 150)

    def getMob(self):
        self.mobLabel = QLabel(self)
        self.mobLabel.setText('Mobile:')
        self.lineMob = QLineEdit(self)
        self.lineMob.move(480, 190)
        self.mobLabel.move(420, 190)

    def read_image(self, image_path):
        return Image.open(image_path)

    def get_base64_form(self):
        buff = io.BytesIO()
        self.image.save(buff, format="JPEG")
        img_str = base64.b64encode(buff.getvalue())
        return img_str

    def get_key_points(self):
        return face_encoding.get_key_points(self.encoded_image)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "jpg file (*.jpg)", options=options)  # nopep8
        if fileName:
            self.image = self.read_image(fileName)
            self.encoded_image = self.get_base64_form()
            self.key_points = self.get_key_points()
            if self.key_points != []:
                label = QLabel(self)
                pixmap = QPixmap(fileName)
                pixmap = pixmap.scaled(280, 350)
                label.setPixmap(pixmap)
                label.resize(280, 350)
                label.move(10, 10)
                label.show()
            else:
                QMessageBox.about(self,
                                  "Error",
                                  "Face not detected")

    def save(self):
        self.mob = self.lineMob.text()
        self.age = self.lineAge.text()
        self.name = self.lineName.text()
        self.father_name = self.lineFName.text()
        self.key_points = face_encoding.encode(self.key_points)
        if db_operations.add_to_pending(self.key_points,
                                        self.name,
                                        self.father_name,
                                        self.age,
                                        self.mob) is True:
            QMessageBox.about(self, "Success", "Image is addes to DB. \
                              You can close the window")
        else:
            QMessageBox.about(self, "Error", "Something went wrong. \
                              Please try again")
