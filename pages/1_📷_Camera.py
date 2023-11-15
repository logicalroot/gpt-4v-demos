import streamlit as st
import base64
import requests
from utils import show_code


def generate(image, api_key):
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
                        "text": """Write your best single-paragraph caption for this image.
                        Do not make assumptions.""",
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

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    )

    st.session_state.camera_caption = response.json()["choices"][0]["message"][
        "content"
    ]


def run():
    bytes_data = None

    uploaded_file = st.camera_input("Take a photo", label_visibility="hidden")
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        st.image(bytes_data, caption=uploaded_file.name, width=200)

    button = st.button(
        "Generate",
        disabled=bytes_data is None or "api_key" not in st.session_state,
        key="generate",
    )

    if button and bytes_data is not None:
        with st.spinner("Generating..."):
            generate(bytes_data, st.session_state.api_key)
            st.balloons()

    if "camera_caption" in st.session_state:
        st.text_area(
            "Caption:",
            st.session_state.camera_caption,
            height=300,
        )


st.set_page_config(page_title="Camera", page_icon="📷")
st.write("# 📷 Camera")
st.write("Take a photo with your device's camera and generate a caption.")
st.info(
    "This is a test of the OpenAI GPT-4V preview and is not intended for production use."
)

run()

show_code([generate, run])
