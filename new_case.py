import os
import shutil
import subprocess
import base64
import io

import cv2
from PIL import Image
import PIL
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QPushButton
from PyQt5.QtWidgets import QInputDialog, QLabel, QLineEdit, QMessageBox

import face_encoding
import db_operations


class NewCase(QMainWindow):
    """
    This class is a subpart of main window.
    The purpose of this class is to register a new case and
    save it in Firebase Database.

    After selecting the image you'll see in left side of window.
    If you are able to see image that means algo is able to find
    facial points in image. Otherwise you'll get error.

    If you encounter any error while saving the image, check the logs
    which are being printed.
    """
    def __init__(self, parent=None):
        """
        We are initializing few things we would need.
            name -> Name of person whose case has to be registered.
            age -> Age of the person
            mob -> Mobile number that will be contacted after the person is found.
            father_name -> Father's name of the person
            image -> image of the person
        """
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
        """
        This method contains button to select the image and
        also register the case.

        The select image button is connected to openFileNameDialog method.

        The save button is connected to save method (within the class).

        -> If you are chaning the window size make sure to align the buttons
            correctly.
        """
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
        """
        This method reads the input name from text field in GUI.
        """
        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Name:')
        self.lineName = QLineEdit(self)
        self.lineName.move(480, 70)
        self.nameLabel.move(420, 70)
        # self.line.resize(200, 32)

    def getAge(self):
        """
        This method reads the age from text field in GUI.
        """
        self.ageLabel = QLabel(self)
        self.ageLabel.setText('Age:')
        self.lineAge = QLineEdit(self)
        self.lineAge.move(480, 110)
        self.ageLabel.move(420, 110)

    def getFName(self):
        """
        This method reads Father's name from text field in GUI.
        """
        self.FnameLabel = QLabel(self)
        self.FnameLabel.setText('Father\'s\n Name:')
        self.lineFName = QLineEdit(self)
        self.lineFName.move(480, 150)
        self.FnameLabel.move(420, 150)

    def getMob(self):
        """
        This method reads mob number from text field in GUI.
        """
        self.mobLabel = QLabel(self)
        self.mobLabel.setText('Mobile:')
        self.lineMob = QLineEdit(self)
        self.lineMob.move(480, 190)
        self.mobLabel.move(420, 190)

    def read_image(self, image_path: str):
        """
        Takes image URL as input and returns image.

        Parameters
        ----------
        image_path: str
            The path of image on local system.

        Returns
        -------
            PIL JPEG Image
        """
        return Image.open(image_path)

    def get_base64_form(self) -> str:
        """
        This method converts the image read by read_image method to string.

        Returns
        -------
        img_str: str
            Image is convterted in base64.
        """
        buff = io.BytesIO()
        self.image.save(buff, format="JPEG")
        img_str = base64.b64encode(buff.getvalue())
        return img_str

    def get_key_points(self) -> list:
        """
        This method passes the base64 form iamge to get facialkey points.

        Returns
        -------
         list
        """
        return face_encoding.get_key_points(self.encoded_image)

    def openFileNameDialog(self):
        """
        This method is triggered on button click to select image.

        When an image is selected its local URL is captured.
        After which it is passed through read_image method.
        Then it is converted to base64 format and facial keypoints are
        generated for it.

        If keypoints are not found in the image then you'll get a dialogbox.
        """
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

    def check_entries(self, mob: str, age: str, name: str, father_name: str) -> bool:
        """
        A check to make sure empty fields are not saved.
        A case will be uniquely identified by these fields. 
        """
        if mob != "" and age != "" and name != "" and father_name != "":
            return True
        else:
            return False

    def save(self):
        """
        Save method is triggered with save button on GUI.
       
        All the parameters are passed to a db methods whose task is to save
        them in db.

        If the save operation is successful then you'll get True as output and
        a dialog message will be displayed other False will be returned and
        you'll get appropriate message.

        """
        self.mob = self.lineMob.text()
        self.age = self.lineAge.text()
        self.name = self.lineName.text()
        self.father_name = self.lineFName.text()
        if self.check_entries(self.mob, self.age, self.name, self.father_name):
            self.key_points = face_encoding.encode(self.key_points)
            if db_operations.add_to_pending(self.key_points,
                                            self.name,
                                            self.father_name,
                                            self.age,
                                            self.mob) is True:
                QMessageBox.about(self, "Success", "Image is added to DB. \n\
                                You can close the window")
            else:
                QMessageBox.about(self, "Error", "Something went wrong. \
                                Please try again")
        else:
            QMessageBox.about(self, "Error", "Please fill all entries")
