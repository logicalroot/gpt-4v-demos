import streamlit as st
import base64
import requests
import json
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
                "content": "You are trained to extract text from images.",
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Extract all of the text visible in this image.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            },
        ],
        "max_tokens": 1024,
    }

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
        )
        response.raise_for_status()

        text = response.json()["choices"][0]["message"]["content"]
        st.session_state.ocr_text = text

        if "balloons" in st.session_state and st.session_state.balloons:
            st.balloons()
    except requests.exceptions.HTTPError as err:
        st.toast(f":red[HTTP error: {err}]")
    except Exception as err:
        st.toast(f":red[Error: {err}]")


def run():
    image = components.image_uploader()

    api_key = components.api_key_with_warning()

    components.submit_button(image, api_key, submit)

    if "ocr_text" in st.session_state:
        st.text_area(
            "Extracted Text",
            st.session_state.ocr_text,
            height=400,
        )


st.set_page_config(page_title="GPT-4V OCR", page_icon="🧾")
components.inc_sidebar_nav_height()
st.write("# 🧾 OCR")
st.write("Extract the text from an image.")
st.info(
    "This is a test of the OpenAI GPT-4V preview and is not intended for production use."
)
st.write("\n")

run()

components.toggle_balloons()
show_code([submit, run, components])
