from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
import sys
from threading import Thread
from uploadNew import *
from train import *
from match_faces import *
class window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Missing Person Application"
        self.initialize()

    def initialize(self):
        self.setWindowTitle(self.title)
        self.setFixedSize(600,400)

        uploadButton = QPushButton("Upload \nnew data",self)
        uploadButton.move(470,100)
        uploadButton.clicked.connect(self.upload)

        updateClsButton = QPushButton("Update\n Database",self)
        updateClsButton.move(470,150)
        updateClsButton.clicked.connect(self.update_DB)

        refreshButton = QPushButton("Refresh",self)
        refreshButton.move(470,200)
        refreshButton.clicked.connect(self.match_faces)

        pendingButton = QPushButton("Pending requests",self)
        pendingButton.move(470,250)
        pendingButton.clicked.connect(self.match)

        confirmedButton = QPushButton("Confirmed requests",self)
        confirmedButton.move(470,300)
        confirmedButton.clicked.connect(self.match)

       

        self.show()

    def upload(self):
        self.u = list()
        u = uploadNewClass()
        self.u.append(u)
        self.show()    

    def match(self):
        pass    

    def update_DB(self):
        t = Thread(target=train)  
        t.start()   

    def match_faces(self):
        matched =  match() 
        print(matched)
          

App = QApplication(sys.argv)
w = window()
sys.exit(App.exec())