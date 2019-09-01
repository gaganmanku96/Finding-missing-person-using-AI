import base64
import time
import os
import pickle
import warnings
import io

import cv2
from PIL import Image
import numpy as np

import face_recognition_api
from train_model import *
from db_operations import *


model_name = 'classifier.pkl'


def decode_base64(img):
    img = img[1:]
    img = np.array(Image.open(io.BytesIO(base64.b64decode(img))))
    return img


def get_facial_points(img):
    return face_recognition_api.face_encodings(img)


def fetch_faces_fromDB(db_name='user'):
    data = []
    result = db.reference(db_name).get()
    for user_id, cases in result.items():
        for case, value in cases.items():
            image = decode_base64(value.get('image'))
            key_pts = get_facial_points(image)
            location = value.get('location')
            data.append([image, key_pts, location])
    return data


def match():
    if os.path.isfile(model_name):
        with open(model_name, 'rb') as f:
            (le, clf) = pickle.load(f)
    else:
        return "None"
    matched = []
    data = fetch_faces_fromDB()
    for image, key_pts, location in data:
        closest_distances = clf.kneighbors(key_pts)
        is_recognized = [closest_distances[0][0][0] <= 0.5]
        # No clue why 'is True' is not working
        if is_recognized[0] == True:
            predictions = [(le.inverse_transform([pred]))
                           if rec else ("Unknown")
                           for pred, rec in zip(clf.predict(key_pts),
                                                is_recognized)]
            matched.append([predictions, image, location])
    return matched
