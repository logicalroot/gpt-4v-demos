import streamlit as st
import base64
import requests
import json
import components
from utils import show_code
from parsers import extract_json


def submit(image, api_key):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    base64_image = base64.b64encode(image).decode("utf-8")

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "system",
                "content": """You are an expert quality control inspector for
                leading manufacturers.""",
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """Inspect this image and write a report in the following
                        JSON format:\n\n
                        {
                            "issues": [
                                {
                                    "issue_found": boolean,
                                    "issue_critical": boolean,
                                    "issue_category": string,
                                    "issue_description": string
                                }
                            ]
                        }\n\n
                        If you see any signs of quality deterioration of any kind,
                        such as mold, physical damage, rot, or corrosion, they must
                        be reported. Multiple issues should be formatted as separate
                        objects in the `issues` array. If there are no issues,
                        the `issues` array should be empty. Your response should
                        contain only valid JSON.""",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            },
        ],
        "max_tokens": 1024,
        # Response format not yet supported by GPT-4V
        # "response_format": {"type": "json_object"},
    }

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
        )
        response.raise_for_status()

        text = extract_json(response.json()["choices"][0]["message"]["content"])
        st.session_state.response_text = text
        st.balloons()
    except requests.exceptions.HTTPError:
        st.toast(f":red[HTTP error. Check your API key.]")
    except Exception as err:
        st.toast(f":red[Error: {err}]")


def run():
    image = components.image_uploader()

    api_key = components.api_key_with_warning()

    components.submit_button(image, api_key, submit)

    if "response_text" in st.session_state:
        st.text_area(
            "Response:",
            st.session_state.response_text,
            height=400,
        )


st.set_page_config(page_title="GPT-4V Quality Control", page_icon="📋")
st.write("# 📋 Quality Control")
st.write("Upload an image and generate a QC report.")
st.info(
    "This is a test of the OpenAI GPT-4V preview and is not intended for production use."
)
st.write("\n")

run()

show_code([submit, run, components])
