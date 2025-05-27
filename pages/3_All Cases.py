import streamlit as st
from pages.helper import db_queries
from pages.helper.streamlit_helpers import require_login


def case_viewer(case):
    case = list(case)
    case_id = case.pop(0)
    matched_with_id = case.pop(-1)
    matched_with_details = None

    try:
        matched_with_id = matched_with_id.replace("{", "").replace("}", "")
    except:
        matched_with = None

    if matched_with_id:
        matched_with_details = db_queries.get_public_case_detail(matched_with_id)

    data_col, image_col, matched_with_col = st.columns(3)
    for text, value in zip(["Name", "Age", "Status", "Last Seen", "Phone"], case):
        if value == "F":
            value = "Found"
        elif value == "NF":
            value = "Not Found"
        data_col.write(f"{text}: {value}")

    image_col.image(
        "./resources/" + str(case_id) + ".jpg",
        width=120,
        use_container_width=False,
    )
    if matched_with_details:
        matched_with_col.write(f"Location: {matched_with_details[0][0]}")
        matched_with_col.write(f"Submitted By: {matched_with_details[0][1]}")
        matched_with_col.write(f"Mobile: {matched_with_details[0][2]}")
        matched_with_col.write(f"Birth Marks: {matched_with_details[0][3]}")
    st.write("---")


def public_case_viewer(case: list) -> None:
    case = list(case)
    case_id = str(case.pop(0))

    data_col, image_col, _ = st.columns(3)
    for text, value in zip(
        ["Status", "Location", "Mobile", "Birth Marks", "Submitted on", "Submitted by"],
        case,
    ):
        if text == "Status":
            value = "Found" if value == "F" else "Not Found"

        data_col.write(f"{text}: {value}")

    try:
        image_col.image(
            "./resources/" + case_id + ".jpg",
            width=120,
            use_container_width=False,
        )
    except Exception as e:
        st.warning("Couldn't load image")

    st.write("---")


if "login_status" not in st.session_state:
    st.write("You don't have access to this page")

elif st.session_state["login_status"]:
    user = st.session_state.user

    st.title("View Submitted Cases")

    status_col, date_col = st.columns(2)
    status = status_col.selectbox(
        "Filter", options=["All", "Not Found", "Found", "Public Cases"]
    )
    date = date_col.date_input("Date")

    if status == "Public Cases":
        cases_data = db_queries.fetch_public_cases(False, status)
        st.write("\n\n")
        st.write("---")
        for case in cases_data:
            public_case_viewer(case)

    else:
        cases_data = db_queries.fetch_registered_cases(user, status)
        st.write("\n\n")
        st.write("---")
        for case in cases_data:
            case_viewer(case)

else:
    st.write("You don't have access to this page")
