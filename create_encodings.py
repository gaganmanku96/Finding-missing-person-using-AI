import os
import face_recognition_api
import pandas as pd
from connect_DB import *


def convert_encoding(encoding):
    st = ""
    encoding = encoding[0]
    for value in encoding:
        svalue = str(value)
        if(value<0):
            svalue = svalue.replace('-','1') # Replace '-' with 1
        svalue = svalue.replace('.','$') # Replace . with $
        st = st+ '@' + svalue # replace 2 values with @   
    return st    

def create_store(fileName,name,fname,age,mob):
    img = face_recognition_api.load_image_file(fileName)
    imgEncoding = face_recognition_api.face_encodings(img)

    if len(imgEncoding) > 1:
        print('More than one face found in the image')
    if len(imgEncoding) == 0:
        print('No Face found in the Image')
    else:
        print('Encoded successfully.')
    encoded = convert_encoding(imgEncoding)   

    name = name.replace(' ','@')
    fname = fname.replace(' ','@')

    print(name)
    print(fname)

    uniqueKey = str(name) + str(age) + str(fname) + str(mob)
    print(uniqueKey)
    
    root = db.reference('stationID')
    new_user = root.child('ABC123').child('pending').child(uniqueKey).set({
        'encoded':encoded
    })
    print('Done')
