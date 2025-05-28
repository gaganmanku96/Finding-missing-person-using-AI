import uuid
import numpy as np
import streamlit as st
import json
import base64

from pages.helper.data_models import RegisteredCases
from pages.helper import db_queries
from pages.helper.utils import image_obj_to_numpy, extract_face_mesh_landmarks
from pages.helper.streamlit_helpers import require_login

st.set_page_config(page_title="Case New Form")


def image_to_base64(image):
    return base64.b64encode(image).decode("utf-8")


if "login_status" not in st.session_state:
    st.write("You don't have access to this page")

elif st.session_state["login_status"]:
    user = st.session_state.user

    st.title("Register New Case")

    image_col, form_col = st.columns(2)
    image_obj = None
    save_flag = 0

    with image_col:
        image_obj = st.file_uploader(
            "Image", type=["jpg", "jpeg", "png"], key="new_case"
        )

        if image_obj:
            import uuid

            unique_id = str(uuid.uuid4())
            uploaded_file_path = "./resources/" + str(unique_id) + ".jpg"
            with open(uploaded_file_path, "wb") as output_temporary_file:
                output_temporary_file.write(image_obj.read())

            with st.spinner("Processing..."):
                st.image(image_obj)
                image_numpy = image_obj_to_numpy(image_obj)
                face_mesh = extract_face_mesh_landmarks(image_numpy)

    if image_obj:
        with form_col.form(key="new_case"):
            name = st.text_input("Name")
            fathers_name = st.text_input("Father's Name")
            age = st.number_input("Age", min_value=3, max_value=100, value=10, step=1)
            mobile_number = st.text_input("Mobile Number")
            address = st.text_input("Address")
            adhaar_card = st.text_input("Adhaar Card")
            birthmarks = st.text_input("Birth Mark")
            last_seen = st.text_input("Last Seen")
            description = st.text_area("Description (optional)")

            complainant_name = st.text_input("Complainant Name")
            complainant_phone = st.text_input("Complainant Phone")

            submit_bt = st.form_submit_button("Save")

            new_case_details = RegisteredCases(
                id=unique_id,
                submitted_by=user,
                name=name,
                fathers_name=fathers_name,
                age=age,
                complainant_mobile=mobile_number,
                complainant_name=complainant_name,
                face_mesh=json.dumps(face_mesh),
                adhaar_card=adhaar_card,
                birth_marks=birthmarks,
                address=address,
                last_seen=last_seen,
                status="NF",
                matched_with="",
            )

            if submit_bt:
                db_queries.register_new_case(new_case_details)
                save_flag = 1

        if save_flag:
            st.success("Case Registered")

else:
    st.write("You don't have access to this page")
