import streamlit as st
from functools import wraps


def require_login(func):
    """Decorator to require login for Streamlit pages."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        if (
            "login_status" not in st.session_state
            or not st.session_state["login_status"]
        ):
            st.write("You don't have access to this page")
            return
        return func(*args, **kwargs)

    return wrapper


def show_success(message: str):
    st.success(message)


def show_error(message: str):
    st.error(message)


def show_warning(message: str):
    st.warning(message)
