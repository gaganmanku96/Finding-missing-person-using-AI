import yaml
import base64
import streamlit as st
from yaml import SafeLoader
import streamlit_authenticator as stauth

from pages.helper import db_queries


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover;
    }}
    </style>
    """,
        unsafe_allow_html=True,
    )


if "login_status" not in st.session_state:
    st.session_state["login_status"] = False

try:
    with open("login_config.yml") as file:
        config = yaml.load(file, Loader=SafeLoader)
except FileNotFoundError:
    st.error("Configuration file 'login_config.yml' not found")
    st.stop()

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
)

# Perform login - this updates session state variables
authenticator.login(location="main")

# Access authentication status from session state
if st.session_state.get("authentication_status"):
    authenticator.logout("Logout", "sidebar")

    st.session_state["login_status"] = True
    user_info = config["credentials"]["usernames"][st.session_state["username"]]
    st.session_state["user"] = user_info["name"]

    st.write(
        f'<p style="color:grey; text-align:left; font-size:45px">{user_info["name"]}</p>',
        unsafe_allow_html=True,
    )

    st.write(
        f'<p style="color:grey; text-align:left; font-size:20px">{user_info["area"]}, {user_info["city"]}</p>',
        unsafe_allow_html=True,
    )

    st.write(
        f'<p style="color:grey; text-align:left; font-size:20px">{user_info["role"]}</p>',
        unsafe_allow_html=True,
    )

    st.write("---")

    found_cases = db_queries.get_registered_cases_count(user_info["name"], "F")
    non_found_cases = db_queries.get_registered_cases_count(user_info["name"], "NF")

    found_col, not_found_col = st.columns(2)

    found_col.metric("Found Cases Count", value=len(found_cases))
    not_found_col.metric("Not Found Cases Count", value=len(non_found_cases))

elif st.session_state.get("authentication_status") == False:
    st.error("Username/password is incorrect")
elif st.session_state.get("authentication_status") == None:
    st.warning("Please enter your username and password")
    st.session_state["login_status"] = False
