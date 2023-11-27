import streamlit as st
import base64
import requests
import json
import components
from utils import show_code
from parsers import extract_json


def submit(image, api_key, issue_attributes):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    base64_image = base64.b64encode(image).decode("utf-8")

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "system",
                "content": "You are an expert quality control inspector for leading manufacturers.",
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Inspect this image and write a report in the following format:\n\n"
                            "```json\n"
                            "{\n"
                            '  "issues": [\n'
                            "    {\n"
                            f"{issue_attributes}\n"
                            "    }\n"
                            "  ]\n"
                            "}\n"
                            "```\n\n"
                            "If you see any signs of quality deterioration of any kind, such as corrosion, "
                            "physical damage, decay, or contamination, add them as separate issues in the "
                            "`issues` array. If there are no issues, the `issues` array should be empty. "
                            "Your response should contain only valid JSON."
                        ),
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            },
        ],
        "max_tokens": 1024,
        "temperature": 0.1,
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

        if "balloons" in st.session_state and st.session_state.balloons:
            st.balloons()
    except requests.exceptions.HTTPError as err:
        st.toast(f":red[HTTP error: {err}]")
    except Exception as err:
        st.toast(f":red[Error: {err}]")


def run():
    image = components.image_uploader()

    issue_attributes = st.text_area(
        "Quality Issue Attributes",
        value='"issue_critical": true if inedible,\n'
        '"issue_category": string,\n'
        '"issue_description": single-paragraph string',
        height=120,
    )

    api_key = components.api_key_with_warning()

    components.submit_button(image, api_key, submit, issue_attributes)

    if "response_text" in st.session_state:
        st.text_area(
            "QC Report",
            st.session_state.response_text,
            height=400,
        )


st.set_page_config(page_title="GPT-4V Quality Control", page_icon="📋")
components.inc_sidebar_nav_height()
st.write("# 📋 Quality Control")
st.write("Generate a QC report for an image.")
st.info(
    "This is a test of the OpenAI GPT-4V preview and is not intended for production use."
)
st.write("\n")

run()

components.toggle_balloons()
show_code([submit, run, components])
