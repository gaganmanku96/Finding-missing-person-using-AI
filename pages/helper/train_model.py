import os
import json
import pickle
import traceback

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier

from pages.helper import db_queries


def get_train_data(submitted_by: str):
    """
    Gets the training data for the user logged in

    Args:
        submitted_by: str
    """

    try:
        result = db_queries.get_training_data(submitted_by)

        d1 = pd.DataFrame(result, columns=["label", "face_mesh"])
        d1["face_mesh"] = d1["face_mesh"].apply(lambda x: json.loads(x))

        d2 = pd.DataFrame(d1.pop("face_mesh").values.tolist(), index=d1.index).rename(
            columns=lambda x: "fm_{}".format(x + 1)
        )
        df = d1.join(d2)
        return df["label"], df.drop("label", axis=1)

    except Exception as e:
        traceback.print_exc()
        raise e


def train(submitted_by: str):
    """
    Trains a KNN Model on the submitted cases.

    Args:
        submitted_by: str

    Returns:
        dict - {
            "status": bool - whether the functional call was successful or not
            "message": str - message returned on each case
        }

    """
    model_name = "classifier.pkl"
    if os.path.isfile(model_name):
        os.remove(model_name)
    try:
        labels, key_pts = get_train_data(submitted_by)
        if len(labels) == 0:
            return {"status": False, "message": "No cases submmited by this user"}
        le = LabelEncoder()
        encoded_labels = le.fit_transform(labels)
        classifier = KNeighborsClassifier(
            n_neighbors=len(labels), algorithm="ball_tree", weights="distance"
        )
        classifier.fit(key_pts, encoded_labels)

        with open(model_name, "wb") as file:
            pickle.dump((le, classifier), file)
        return {"status": True, "message": "Model Refreshed"}
    except Exception as e:
        traceback.print_exc()
        return {"status": False, "message": str(e)}


if __name__ == "__main__":
    result = train("admin")
