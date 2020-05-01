# Finding missing people through AI

### Please read the LICENCE before using this project.

## Introduction
This project is about how we can locate missing persons with the help of AI.\
The project contains 2 different applications - 1. Desktop (build using PyQT5)\
and 2. Android Application. The Desktop app can only be accessed by authoried person
while the android app can be accessed by anyone.

Let's start with a story. A boy goes missing and his parents want to register a \
complaint. They will go to the person whole is authorized for managing the \
desktop app. The authorized person will register a complaint. Now comes the part 
of android app. The android app will be used by common people who can submit any 
picture. These pictures will be of people who they find suspicious or doubtful.
The authorized person with the click of a button can check if any registered person
matched the picture submitted by common people. If match is found then it's last location
is shown which can help to track him.

### Why do we need such thing?

1. [India’s missing children: The story WhatsApp forwards don’t tell you](https://www.thehindu.com/society/indias-missing-children-what-the-whatsapp-rumours-dont-tell-you/article24641527.ece)
2. [India’s children: 174 go missing every day, half untraced](https://www.deccanchronicle.com/nation/current-affairs/250518/indias-children-174-go-missing-every-day-half-untraced.html)


## Getting Started
### Requirements
1. Python 3.4+ (Conda environment favoured)
2. Firebase Database
3. OpenCV, PyQT5, dlib

### Installing 
* Download Miniconda (don't go for latest version as it might be incompatible with dlib). The tested version is Miniconda3-4.2.11.
* Install following dependencies
```
$ conda install -c conda-forge dlib 
$ pip install pyqt5
$ pip install opencv-python
$ pip install firebase_admin
$ pip install pillow
```
* Setup Firebase Realtime database
    1. Open firebase.google.com
    2. Create a new project
    3. Go to Database and then realtime database
    4. Copy Project URL and download key from project setting.
    5. Replace Project URL and key location in db_operations file

### Android App
I couldn't find the source code for the android file.
But I created a python script through which you upload photos.
It will always be better if you could build android app for it.
The file is upload_user_image.py and replace the URL in it.

## Running the application
How to start the project?

1. Clone the Repository
2. Go inside the folder
3. Open cmd in the same directory
4. Activate conda environment (if you are using environment other than base)
5. Type python main.py
6. If everything is fine you'll see a GUI window in few seconds.
 
## Contributions
I'm looking for people who can help me in developing a web app for it.
The app needs to be redesigned due to lot of performance constrains. 

#### Vote of Thanks
- Thanks to [Davis King](https://github.com/davisking) for creating dlib and for providing the trained facial feature
  detection and face encoding models used in this project.
