import streamlit as st
import base64
import requests
import components
from utils import show_code


def submit(image, api_key):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    base64_image = base64.b64encode(image).decode("utf-8")

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "system",
                "content": "You are a friendly assistant.",
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Write your best four-sentence caption for this image, highlighting the most "
                        "interesting aspects without making assumptions.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            },
        ],
        "max_tokens": 300,
    }

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
        )
        response.raise_for_status()

        camera_caption = response.json()["choices"][0]["message"]["content"]
        st.session_state.camera_caption = camera_caption

        if "balloons" in st.session_state and st.session_state.balloons:
            st.balloons()
    except requests.exceptions.HTTPError as err:
        st.toast(f":red[HTTP error: {err}]")
    except Exception as err:
        st.toast(f":red[Error: {err}]")


def run():
    selected_option = st.radio(
        "Image Input",
        ["Camera", "Image File"],
        horizontal=True,
        label_visibility="collapsed",
    )

    if selected_option == "Camera":
        image = components.camera_uploader()
    else:
        image = components.image_uploader()

    api_key = components.api_key_with_warning()

    components.submit_button(image, api_key, submit)

    if "camera_caption" in st.session_state:
        st.text_area(
            "Caption",
            st.session_state.camera_caption,
            height=300,
        )


st.set_page_config(page_title="GPT-4V Camera", page_icon="📷")
components.inc_sidebar_nav_height()
st.write("# 📷 Camera")
st.write("Take a photo with your device's camera and generate a caption.")
st.info(
    "This is a test of the OpenAI GPT-4V preview and is not intended for production use."
)

run()

components.toggle_balloons()
show_code([submit, run, components])
