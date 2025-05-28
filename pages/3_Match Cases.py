import streamlit as st

from pages.helper import db_queries, match_algo, train_model
from pages.helper.streamlit_helpers import require_login


def case_viewer(registered_case_id, public_case_id):
    try:
        # Use IDs directly as strings (no UUID conversion needed)
        # Get case details using the string IDs
        case_details = db_queries.get_registered_case_detail(registered_case_id)[0]
        data_col, image_col = st.columns(2)
        for text, value in zip(
            ["Name", "Mobile", "Age", "Last Seen", "Birth marks"], case_details
        ):
            data_col.write(f"{text}: {value}")

        # Update status with properly formatted UUIDs
        db_queries.update_found_status(registered_case_id, public_case_id)
        st.success(
            "Status Changed. Next time it will be only visible in confirmed cases page"
        )

        # Display image
        try:
            image_col.image(
                "./resources/" + registered_case_id + ".jpg",
                width=80,
                use_container_width=False,
            )
        except Exception as img_err:
            st.warning(f"Could not load image: {str(img_err)}")

    except Exception as e:
        import traceback

        traceback.print_exc()
        st.error(f"Something went wrong: {str(e)}. Please check logs")


if "login_status" not in st.session_state:
    st.write("You don't have access to this page")

elif st.session_state["login_status"]:
    user = st.session_state.user

    st.title("Check for match")

    col1, col2 = st.columns(2)

    refresh_bt = col1.button("Refresh")
    st.write("---")

    if refresh_bt:
        with st.spinner("Fetching Data and Training Model..."):
            result = train_model.train(user)

            matched_ids = match_algo.match()

            if matched_ids["status"]:
                if not matched_ids["result"]:
                    st.info("No match found")
                else:
                    for matched_id, submitted_case_id in matched_ids["result"].items():
                        case_viewer(matched_id, submitted_case_id[0])
                        st.write("---")
            else:
                st.info("No match found")

else:
    st.write("You don't have access to this page")
