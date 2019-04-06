from PyQt5.QtWidgets import QMainWindow,QFileDialog,QPushButton, QInputDialog, QLabel,QLineEdit, QMessageBox
from PyQt5.QtGui import QPixmap
import os
import shutil
import subprocess
from create_encodings import *
import time
class uploadNewClass(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "Upload new Information"
        self.name = ""
        self.age = ""
        self.mob = ""
        self.fileName = ""
        self.fname = ""
        self.ImageCompiled = False
        self.initialize()
    def initialize(self):
        self.setFixedSize(600,400)
        self.setWindowTitle(self.title) 
        
        uploadImageBT = QPushButton("select image file",self)
        uploadImageBT.move(400,20)
        uploadImageBT.clicked.connect(self.openFileNameDialog)
        uploadImageBT.setStyleSheet(
             "QPushButton:pressed{color: red} QPushButton{color: black}")

        saveBT = QPushButton("Save ",self)
        saveBT.move(400,350)
        saveBT.clicked.connect(self.save)
        saveBT.setStyleSheet(
             "QPushButton:pressed{color: red} QPushButton{color: black}")

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
        #self.line.resize(200, 32)

        

    def getAge(self):
        self.ageLabel = QLabel(self)
        self.ageLabel.setText('Age:')
        self.lineAge = QLineEdit(self)
        self.lineAge.move(480, 110)        
        self.ageLabel.move(420, 110)
        #self.line.resize(200, 32)

    def getFName(self):
        self.FnameLabel = QLabel(self)
        self.FnameLabel.setText('Father\'s\n Name:')
        self.lineFName = QLineEdit(self)
        self.lineFName.move(480, 150)        
        self.FnameLabel.move(420, 150)
        #self.line.resize(200, 32)   

        

    def getMob(self):
        self.mobLabel = QLabel(self)
        self.mobLabel.setText('Mobile:')
        self.lineMob = QLineEdit(self)
        self.lineMob.move(480, 190)        
        self.mobLabel.move(420, 190)
        #self.line.resize(200, 32)

        

    def save(self):

        self.mob = self.lineMob.text()
        self.age = self.lineAge.text()    
        self.name = self.lineName.text()
        self.fname = self.lineFName.text()

               
        self.compile()

    
       
    def compile(self):
        s = create_store(self.fileName,self.name,self.fname,self.mob,self.age)
        if s=="YES":
            QMessageBox.about(self,"Success","Image is addes to DB\nYou can close the window")
        else:
            QMessageBox.about(self,"Error","Something went wrong\nPlease try again")

    def openFileNameDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","png file (*.png);;jpg file (*.jpg)", options=options)
        self.fileName = fileName
        print(self.fileName)
        if fileName:
            label = QLabel(self)
            pixmap = QPixmap(fileName)
            pixmap = pixmap.scaled(280, 350)
            label.setPixmap(pixmap)
            label.resize(280,350)
            label.move(10,10)
            label.show()
            

           
      