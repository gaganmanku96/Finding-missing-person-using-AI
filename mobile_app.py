import uuid
import json

import streamlit as st
import uuid
import json
import numpy as np

from pages.helper import db_queries
from pages.helper.data_models import PublicSubmissions
from pages.helper.utils import image_obj_to_numpy, extract_face_mesh_landmarks
from pages.helper.streamlit_helpers import require_login

st.set_page_config("Mobile UI", initial_sidebar_state="collapsed")


st.title("Make a submission")


image_col, form_col = st.columns(2)
image_obj = None
save_flag = 0

with image_col:
    image_obj = st.file_uploader(
        "Image", type=["jpg", "jpeg", "png"], key="user_submission"
    )
    if image_obj:
        import uuid

        unique_id = str(uuid.uuid4())

        with st.spinner("Processing..."):
            uploaded_file_path = "./resources/" + str(unique_id) + ".jpg"
            with open(uploaded_file_path, "wb") as output_temporary_file:
                output_temporary_file.write(image_obj.read())

            st.image(image_obj, width=200)
            image_numpy = image_obj_to_numpy(image_obj)
            face_mesh = extract_face_mesh_landmarks(image_numpy)

if image_obj:
    with form_col.form(key="new_user_submission"):
        name = st.text_input("Your Name")
        mobile_number = st.text_input("Your Mobile Number")
        email = st.text_input("Your Email")
        address = st.text_input("Address/Location last seen")
        birth_marks = st.text_input("Birth Marks")

        submit_bt = st.form_submit_button("Submit")

        public_submission_details = PublicSubmissions(
            submitted_by=name,
            location=address,
            email=email,
            face_mesh=json.dumps(face_mesh),
            id=unique_id,
            mobile=mobile_number,
            birth_marks=birth_marks,
            status="NF",
        )

        if submit_bt:
            db_queries.new_public_case(public_submission_details)
            save_flag = 1

    if save_flag == 1:
        st.success("Successfully Submitted")
