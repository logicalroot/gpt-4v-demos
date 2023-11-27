import streamlit as st


def api_key_with_warning():
    api_key = (
        st.session_state.api_key
        if "api_key" in st.session_state and st.session_state.api_key != ""
        else None
    )

    if api_key is None:
        st.warning(
            "Input your OpenAI API key in the sidebar on the Home page.", icon="⚠️"
        )

    return api_key


def uploader(file, download=False):
    bytes_data = None

    if file is not None:
        bytes_data = file.getvalue()
        st.image(bytes_data, caption=file.name, width=200)
        if download:
            st.download_button(
                label="📥 Save File",
                data=bytes_data,
                file_name=file.name,
                mime=file.type,
            )

    return bytes_data


def image_uploader():
    return uploader(st.file_uploader("Image file:", label_visibility="collapsed"))


def camera_uploader():
    return uploader(st.camera_input("Take a photo", label_visibility="collapsed"), True)


def submit_button(image, api_key, callback, *optional_parameters):
    button = st.button(
        "Submit",
        disabled=image is None or api_key is None,
        key="submit",
        type="primary",
    )

    if button:
        with st.spinner("Submitting..."):
            if optional_parameters:
                callback(image, api_key, *optional_parameters)
            else:
                callback(image, api_key)


def inc_sidebar_nav_height():
    st.markdown(
        """<style>
        [data-testid="stSidebarNavItems"] {
            max-height: 60vh;
        }
        </style>""",
        unsafe_allow_html=True,
    )


def toggle_balloons():
    st.session_state.balloons = st.sidebar.checkbox("Show balloons", True)
