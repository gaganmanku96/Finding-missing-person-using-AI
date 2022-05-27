import logging

import dlib
import cv2
import numpy as np

face_detector = dlib.get_frontal_face_detector()

predictor_model = "models/shape_predictor_68_face_landmarks.dat"
pose_predictor = dlib.shape_predictor(predictor_model)

face_recognition_model = "models/dlib_face_recognition_resnet_model_v1.dat"
face_encoder = dlib.face_recognition_model_v1(face_recognition_model)


def load_image_file(image, mode="RGB"):
    """
    Loads an image file (.jpg, .png, etc) into a numpy array

    :param filename: image file to loady
    :param mode: format to convert the image to. Only 'RGB' (8-bit RGB, 3 channels) and 'L' (black and white) are supported.
    :return: image contents as numpy array
    """
    # If very large size image, Resize the image
    img = image
    if img.shape[0] > 800:
        baseheight = 500
        w = baseheight / img.shape[0]
        p = int(img.shape[1] * w)
        img = cv2.resize(img, (baseheight, p))
    elif img.shape[1] > 800:
        baseheight = 500
        w = baseheight / img.shape[1]
        p = int(img.shape[0] * w)
        img = cv2.resize(img, (p, baseheight))

    return img


def _tuple_to_rect(rect):
    """
    Convert a tuple in (top, right, bottom, left) order to a dlib `rect` object

    :param rect:  plain tuple representation of the rect in (top, right, bottom, left) order
    :return: a dlib `rect` object
    """
    return dlib.rectangle(rect[3], rect[0], rect[1], rect[2])


def _raw_face_locations(img, number_of_times_to_upsample=1):
    """
    Returns an array of bounding boxes of human faces in a image

    :param img: An image (as a numpy array)
    :param number_of_times_to_upsample: How many times to upsample the image looking for faces. Higher numbers find smaller faces.
    :return: A list of dlib 'rect' objects of found face locations
    """
    return face_detector(img, number_of_times_to_upsample)


def _raw_face_landmarks(face_image, face_locations=None):
    if face_locations is None:
        face_locations = _raw_face_locations(face_image)
    else:
        face_locations = [
            _tuple_to_rect(face_location) for face_location in face_locations
        ]

    return [
        pose_predictor(face_image, face_location) for face_location in face_locations
    ]


def face_encodings(face_image, known_face_locations=None, num_jitters=1):
    """
    Given an image, return the 128-dimension face encoding for each face in the image.

    :param face_image: The image that contains one or more faces
    :param known_face_locations: Optional - the bounding boxes of each face if you already know them.
    :param num_jitters: How many times to re-sample the face when calculating encoding. Higher is more accurate, but slower (i.e. 100 is 100x slower)
    :return: A list of 128-dimentional face encodings (one for each face in the image)
    """
    raw_landmarks = _raw_face_landmarks(face_image, known_face_locations)

    return [
        np.array(
            face_encoder.compute_face_descriptor(
                face_image, raw_landmark_set, num_jitters
            )
        )
        for raw_landmark_set in raw_landmarks
    ]


def get_encoding(image):
    try:
        img = load_image_file(image)
        key_points = list(face_encodings(img)[0])
        return key_points
    except Exception as e:
        print(e)
        return None
