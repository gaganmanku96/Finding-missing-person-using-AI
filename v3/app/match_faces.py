import os
import requests
import json
import pickle
from collections import defaultdict

import pandas as pd
import numpy as np


def get_user_submitted_data(status="NR"):
    url = 'http://localhost:8000/user_submission'
    try:
        result = requests.get(url)
        if result.status_code == 200:
            result = json.loads(result.text)
            d1 = pd.DataFrame(result, columns=['label', 'face_encoding'])
            d2 = (pd.DataFrame(d1.pop('face_encoding').values.tolist(), index=d1.index).rename(columns = lambda x: 'fe_{}'.format(x+1)))
            df = d1.join(d2)
            return df
    except Exception as e:
        raise e


def match():
    model_name = 'classifier.pkl'
    matched_images = defaultdict(list)
    user_submissions_df = get_user_submitted_data()


    if len(user_submissions_df) == 0:
        return {
            "status": False,
            "message": "No submissions found"
        }

    if os.path.isfile(model_name):
        with open(model_name, 'rb') as f:
            (le, clf) = pickle.load(f)
    else:
        return {
            "status": False,
            "message": "Please refresh model"
        }
    
    for row in user_submissions_df.iterrows():
        label = row[1][0]
        face_encoding = row[1][1:]
        closest_distances = clf.kneighbors([face_encoding])
        closest_distance = np.argmin(closest_distances[0][0])
        if closest_distance <= 0.5:
            predicted_label = clf.predict([face_encoding])
            inversed_label = le.inverse_transform([predicted_label])[0]
            matched_images[inversed_label].append(label)

    return {
        "status": True,
        "result": matched_images
    }

if __name__ == "__main__":
    result = (match())
    print(result)
