import streamlit as st
import base64
import requests
import json
import components
from utils import show_code


def submit(image, api_key, product_attributes):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    base64_image = base64.b64encode(image).decode("utf-8")

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "system",
                "content": "You are an expert copywriter for leading brands.",
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""Write your best single-paragraph product description
                        for this image. You are encouraged to incorporate the product
                        attributes provided below. Do not infer sizing, product name,
                        product brand, or specific materials unless provided in the product
                        attributes.\n\n{product_attributes}""",
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

        description = {
            **json.loads(product_attributes),
            "product_description": response.json()["choices"][0]["message"]["content"],
        }
        st.session_state.product_description = json.dumps(
            description, indent=4, ensure_ascii=False
        )
        st.balloons()
    except requests.exceptions.HTTPError:
        st.toast(f":red[HTTP error. Check your API key.]")
    except Exception as err:
        st.toast(f":red[Error: {err}]")


def run():
    image = components.image_uploader()

    product_attributes = st.text_area(
        "Product attributes:",
        value=json.dumps(
            {
                "product_attributes": {
                    "brand_name": "",
                    "product_name": "",
                    "materials": "",
                }
            },
            indent=4,
        ),
        height=200,
    )

    st.caption("Attributes are optional. Feel free to try your own!")

    api_key = components.api_key_with_warning()

    components.submit_button(image, api_key, submit, product_attributes)

    if "product_description" in st.session_state:
        st.text_area(
            "Product attributes with description:",
            st.session_state.product_description,
            height=400,
        )


st.set_page_config(page_title="GPT-4V Product Descriptions", page_icon="👕")
st.write("# 👕 Product Descriptions")
st.write("Upload an image and generate a product description.")
st.info(
    "This is a test of the OpenAI GPT-4V preview and is not intended for production use."
)
st.write("\n")

run()

show_code([submit, run, components])
