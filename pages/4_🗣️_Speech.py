import streamlit as st
import base64
import requests
import json
import components
from utils import show_code


def submit(image, api_key, voice, hd):
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
                        "text": "Extract all of the text visible in this image, ignoring extraneous "
                        "pieces of text like titles and page numbers, and converting Roman numerals "
                        "to Latin numerals. Your response should contain only the headers and content.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            },
        ],
        "max_tokens": 2048,
    }

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
        )
        response.raise_for_status()

        text = response.json()["choices"][0]["message"]["content"]
        st.session_state.extracted_text = text

        tts_payload = {
            "model": "tts-1-hd" if hd else "tts-1",
            "voice": voice,
            "input": text,
        }

        tts_response = requests.post(
            "https://api.openai.com/v1/audio/speech", headers=headers, json=tts_payload
        )
        tts_response.raise_for_status()

        st.audio(tts_response.content, format="audio/mpeg")

        st.download_button(
            label="📥 Save Audio",
            data=tts_response.content,
            file_name=f'audio_{tts_response.headers["x-request-id"]}.mp3',
            mime="audio/mpeg",
        )

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

    voice = st.selectbox(
        "AI Voice",
        ("echo", "alloy", "fable", "onyx", "nova", "shimmer"),
    )

    hd = st.checkbox(
        "HD",
        value=True,
    )

    components.submit_button(image, api_key, submit, voice, hd)

    if "extracted_text" in st.session_state:
        st.text_area(
            "Extracted Text",
            st.session_state.extracted_text,
            height=400,
        )


st.set_page_config(page_title="GPT-4V Speech", page_icon="🗣️")
components.inc_sidebar_nav_height()
st.write("# 🗣️ Speech")
st.write("Generate audio from an image using GPT-4V + OpenAI TTS.")
st.info(
    "This is a test of the OpenAI GPT-4V preview and is not intended for production use."
)
st.write("\n")

run()

components.toggle_balloons()
show_code([submit, run, components])
