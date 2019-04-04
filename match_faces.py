from connect_DB import *
import base64
import cv2
import time
import os
import pickle
import face_recognition_api
import warnings

model_name = 'classifier.pkl'

if os.path.isfile(model_name):
    with open(model_name, 'rb') as f:
        (le, clf) = pickle.load(f)
else:
    print("Classifier '{}' does not exist".format(model_name))
    quit()



def fetch_faces_fromDB(db_name = 'user'):
    data = {}
    if os.path.exists('images'):
        pass
    else:
        os.mkdir('images')     
    os.chdir('images')
    print(os.getcwd())      
    result = db.reference(db_name).get()
    for userID, value in result.items():
        for case, v1 in value.items():
            imgdata = base64.b64decode(v1.get('image'))
            filename = case + str(time.time())[:5]+'.jpg' # I assume you have a way of picking unique filenames
            with open(filename, 'wb') as f:
                f.write(imgdata)

def find_key_pts():
    key_pts = []
    images = os.listdir('images')
    for image in images:
        path = os.path.join('images',image)
        img = face_recognition_api.load_image_file(path)
        # X_faces_loc = face_recognition_api.face_locations(img)
        # faces_encodings = face_recognition_api.face_encodings(img, known_face_locations=X_faces_loc)
        faces_encodings = face_recognition_api.face_encodings(img)
        key_pts.append(faces_encodings)

        
    return key_pts

def match():
    key_pts = find_key_pts()
    for key in key_pts:
        closest_distances = clf.kneighbors(key)

        # is_recognized = [closest_distances[0][i][0] <= 0.5 for i in range(len(X_faces_loc))]
        is_recognized = [closest_distances[0][0][0] <= 0.5]
        if is_recognized:
            predictions = [(le.inverse_transform(int(pred)).title()) if rec else ("Unknown", loc) for pred, rec in
                    zip(clf.predict(key), is_recognized)]

            print(predictions)            
        



match()


