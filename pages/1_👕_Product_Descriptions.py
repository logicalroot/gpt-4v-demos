import streamlit as st
import base64
import requests
import json
import components
from utils import show_code


def submit(image, api_key, product):
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
                        "text": "Write your best single-paragraph product description for this image. "
                        "You are encouraged to incorporate the product attributes provided below. "
                        "Do not infer sizing, product name, product brand, or specific materials unless "
                        "provided in the product attributes. Make sure to write about the colors and "
                        "other visible features of the product.\n\n"
                        f"{product}",
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

        description = response.json()["choices"][0]["message"]["content"]
        product = json.loads(product)
        description = (
            description.replace(" '", " ")
            .replace("' ", " ")
            .replace(' "', " ")
            .replace('" ', " ")
        )
        product["product_attributes"]["description"] = description
        st.session_state.product = json.dumps(product, indent=4, ensure_ascii=False)

        if "balloons" in st.session_state and st.session_state.balloons:
            st.balloons()
    except requests.exceptions.HTTPError as err:
        st.toast(f":red[HTTP error: {err}]")
    except Exception as err:
        st.toast(f":red[Error: {err}]")


def run():
    image = components.image_uploader()

    product = st.text_area(
        "Product Attributes",
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

    components.submit_button(image, api_key, submit, product)

    if "product" in st.session_state:
        st.text_area(
            "Product Attributes With Description",
            st.session_state.product,
            height=400,
        )


st.set_page_config(page_title="GPT-4V Product Descriptions", page_icon="👕")
components.inc_sidebar_nav_height()
st.write("# 👕 Product Descriptions")
st.write("Generate a product description for an image.")
st.info(
    "This is a test of the OpenAI GPT-4V preview and is not intended for production use."
)
st.write("\n")

run()

components.toggle_balloons()
show_code([submit, run, components])
