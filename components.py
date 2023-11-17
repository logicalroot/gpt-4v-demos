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


def uploader(file):
    bytes_data = None

    if file is not None:
        bytes_data = file.getvalue()
        st.image(bytes_data, caption=file.name, width=200)

    return bytes_data


def image_uploader():
    return uploader(st.file_uploader("Image file:"))


def camera_uploader():
    return uploader(st.camera_input("Take a photo", label_visibility="hidden"))


def submit_button(image, api_key, callback, *optional_parameters):
    button = st.button(
        "Submit",
        disabled=image is None or api_key is None,
        key="submit",
    )

    if button:
        with st.spinner("Submitting..."):
            if optional_parameters:
                callback(image, api_key, *optional_parameters)
            else:
                callback(image, api_key)
