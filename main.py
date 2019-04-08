from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QListView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
import sys
from threading import Thread
from uploadNew import *
from train import *
from match_faces import *
from PIL import Image
import cv2
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

        updateClsButton = QPushButton("Update\n Classifier",self)
        updateClsButton.move(470,150)
        updateClsButton.clicked.connect(self.update_DB)

        refreshButton = QPushButton("Match",self)
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
        list = QListView(self)
        list.setIconSize(QSize(72,72))
        list.setMinimumSize(400, 380)
        model = QStandardItemModel(list)
        for person in matched:
            label, img_ = person
            label = label[0].split('@')
            try:
                name_ = label[0]
                mobile = label[1]
                fname_ = label[2]
                age = label[3]
                name_ = name_.split('*')
                try:
                    name = name_[0] + " " +name_[1]
                except:
                    name = name_[0]        
                fname_ = fname_.split('*')
                try:
                    fname = fname_[0] + " " + fname_[1]
                except:
                    fname = fname_[0]
                
                item1 = QStandardItem("  Name                   : "+name+
                                    "\n  Father's Name    : "+fname+
                                    "\n  Age                      : "+age+
                                    "\n  Mobile                 : "+mobile )
                
                icon = QPixmap(os.path.join('images',img_))

                item1.setIcon(QIcon(icon))               
                model.appendRow(item1)  
                
            except:
                print("Error in match_faces function")
            

        
        list.setModel(model)
        list.show()

App = QApplication(sys.argv)
w = window()
sys.exit(App.exec())