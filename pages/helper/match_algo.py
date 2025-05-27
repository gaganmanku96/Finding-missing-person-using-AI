import os
import pickle
import json
import traceback
import warnings
from collections import defaultdict

import pandas as pd
import numpy as np
from sklearn.exceptions import DataConversionWarning

warnings.filterwarnings(action="ignore", category=DataConversionWarning)


from pages.helper import db_queries


def get_public_cases_data(status="NF"):
    try:
        result = db_queries.fetch_public_cases(train_data=True, status=status)
        d1 = pd.DataFrame(result, columns=["label", "face_mesh"])
        d1["face_mesh"] = d1["face_mesh"].apply(lambda x: json.loads(x))
        d2 = pd.DataFrame(d1.pop("face_mesh").values.tolist(), index=d1.index).rename(
            columns=lambda x: "fm_{}".format(x + 1)
        )
        df = d1.join(d2)
        return df

    except Exception as e:
        traceback.print_exc()
        return None


def match(threshold=0.1):
    from scipy.spatial.distance import euclidean

    matched_images = defaultdict(list)
    user_submissions_df = get_public_cases_data()

    if user_submissions_df is None:
        return {"status": False, "message": "Couldn't connect to database"}

    if len(user_submissions_df) == 0:
        return {"status": False, "message": "No submissions found"}

    # Compare each pair (brute force, can optimize)
    for i, row1 in user_submissions_df.iterrows():
        label1 = row1[0]
        mesh1 = np.array(row1[1:]).astype(float)
        for j, row2 in user_submissions_df.iterrows():
            if i >= j:
                continue
            label2 = row2[0]
            mesh2 = np.array(row2[1:]).astype(float)
            dist = euclidean(mesh1, mesh2)
            if dist < threshold:
                matched_images[label1].append(label2)
                matched_images[label2].append(label1)

    return {"status": True, "result": matched_images}


if __name__ == "__main__":
    result = match()
    print(result)
