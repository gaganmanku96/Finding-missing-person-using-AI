import pickle
import os

from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier

import db_operations
import face_encoding

model_name = "classifier.pkl"


def fetch_data():
    labels = []
    key_points = []
    result = db_operations.fetch_pending_cases()
    for unique_label, encoded_image in result.items():
        labels.append(unique_label)
        decoded_image = face_encoding.decode(encoded_image['encoded'])
        key_points.append(decoded_image)
    return labels, key_points


def train_model():
    if os.path.isfile('classifier.pkl'):
        os.remove('classifier.pkl')
    try:
        labels, key_pts = fetch_data()
        le = LabelEncoder()
        encoded_labels = le.fit_transform(labels)

        classifier = KNeighborsClassifier(n_neighbors=len(labels),
                                          algorithm='ball_tree',
                                          weights='distance')
        classifier.fit(key_pts, encoded_labels)

        with open(model_name, 'wb') as file:
            pickle.dump((le, classifier), file)
        return True
    except Exception as e:
        print(str(e))
        return False
