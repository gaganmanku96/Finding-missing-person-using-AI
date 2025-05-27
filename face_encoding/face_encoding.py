import logging
import os
import traceback
from typing import Union

import dlib
import cv2
import numpy as np


class FaceEncoding:
    def __init__(self, model_path: str = "models/") -> None:
        self._model_path = model_path
        self._load_model()

    def _load_model(self):
        model_files = [
            "shape_predictor_68_face_landmarks.dat",
            "dlib_face_recognition_resnet_model_v1.dat",
        ]
        if (model_files[0] not in os.listdir(self._model_path)) or (
            model_files[1] not in os.listdir(self._model_path)
        ):
            raise ValueError(
                f"Couldn't find models in {self._model_path}. Please check file names -> {', '.join(model_files)}"
            )

        self._pose_predictor = dlib.shape_predictor(
            os.path.join(self._model_path, model_files[0])
        )
        self._face_encoder_model = dlib.face_recognition_model_v1(
            os.path.join(self._model_path, model_files[1])
        )
        self._face_detector = dlib.get_frontal_face_detector()

    def crop_image(self, image: np.array) -> np.array:
        if image.shape[0] > 800:
            baseheight = 500
            w = baseheight / image.shape[0]
            p = int(image.shape[1] * w)
            image = cv2.resize(image, (baseheight, p))
        elif image.shape[1] > 800:
            baseheight = 500
            w = baseheight / image.shape[1]
            p = int(image.shape[0] * w)
            image = cv2.resize(image, (p, baseheight))
        return image

    def _raw_face_locations(
        self, image: np.array, number_of_times_to_upsample: int = 1
    ):
        """
        Returns an array of bounding boxes of human faces in a image

        Args:
            image (np.array): An image
            number_of_times_to_upsample (int): How many times to upsample the image looking for faces. Higher numbers find smaller faces.

        Returns:
            A list of dlib 'rect' objects of found face locations
        """
        return self._face_detector(image, number_of_times_to_upsample)

    def _raw_face_landmarks(self, face_image: np.array, face_locations=None):
        if face_locations is None:
            face_locations = self._raw_face_locations(face_image)
        else:
            face_locations = [
                self._tuple_to_rect(face_location) for face_location in face_locations
            ]

        return [
            self._pose_predictor(face_image, face_location)
            for face_location in face_locations
        ]

    def _tuple_to_rect(rect: tuple) -> dlib.rectangle:
        """
        Convert a tuple in (top, right, bottom, left) order to a dlib `rect` object

        Args:
            rect (tuple):  plain tuple representation of the rect in (top, right, bottom, left) order

        Return: a dlib `rect` object
        """
        return dlib.rectangle(rect[3], rect[0], rect[1], rect[2])

    def _face_encodings(self, face_image, known_face_locations=None, num_jitters=1):
        """
        Given an image, return the 128-dimension face encoding for each face in the image.

        :param face_image: The image that contains one or more faces
        :param known_face_locations: Optional - the bounding boxes of each face if you already know them.
        :param num_jitters: How many times to re-sample the face when calculating encoding. Higher is more accurate, but slower (i.e. 100 is 100x slower)
        :return: A list of 128-dimentional face encodings (one for each face in the image)
        """
        raw_landmarks = self._raw_face_landmarks(face_image, known_face_locations)
        return [
            np.array(
                self._face_encoder_model.compute_face_descriptor(
                    face_image, raw_landmark_set, num_jitters
                )
            )
            for raw_landmark_set in raw_landmarks
        ]

    def predict(self, image: np.array) -> Union[list, None]:
        try:
            cropped_image = self.crop_image(image)
            key_points = list(self._face_encodings(cropped_image)[0])
            return key_points
        except IndexError:
            raise IndexError("No keypoints found")
        except Exception as e:
            raise Exception("Unknow error occured")
            # traceback.print_exc()
