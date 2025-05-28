import PIL
import numpy as np
import streamlit as st
import mediapipe as mp


def image_obj_to_numpy(image_obj) -> np.ndarray:
    """Convert a Streamlit-uploaded image object to a numpy array."""
    image = PIL.Image.open(image_obj)
    return np.array(image)


def extract_face_mesh_landmarks(image: np.ndarray):
    """
    Extract face mesh landmarks from an image using MediaPipe.
    Returns a flattened list of all (x, y, z) landmarks if a face is found, else None.
    """
    mp_face_mesh = mp.solutions.face_mesh
    with mp_face_mesh.FaceMesh(
        static_image_mode=True, max_num_faces=1, refine_landmarks=True
    ) as face_mesh:
        results = face_mesh.process(image)
        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark
            # Flatten all landmarks into a single list [x1, y1, z1, x2, y2, z2, ...]
            return [coord for lm in landmarks for coord in (lm.x, lm.y, lm.z)]
        else:
            st.error("Couldn't find face mesh in image. Please try another image.")
            return None
