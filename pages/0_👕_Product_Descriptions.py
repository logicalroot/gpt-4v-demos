import streamlit as st
import base64
import requests
import json
from utils import show_code


def generate(image, api_key, product_attributes="{}"):
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
                        attributes below. Do not infer sizing, product name, product
                        brand, or specific materials unless provided in the product
                        attributes below. If the materials are a blend, refrain
                        from citing specific values. Do not infer anything about
                        the brand from its name.\n\n{product_attributes}""",
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

    description = {
        **json.loads(product_attributes),
        "description": response.json()["choices"][0]["message"]["content"],
    }
    st.session_state.product_description = json.dumps(description, indent=4)


def run():
    bytes_data = None

    uploaded_file = st.file_uploader("Image file:")
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        st.image(bytes_data, caption=uploaded_file.name, width=200)

    product_attributes = st.text_area(
        "Product attributes:",
        value='{\n  "brand_name": "",\n  "product_name": "",\n  "materials": ""\n}',
        height=200,
    )

    st.caption("Attributes are optional. Feel free to try your own!")

    button = st.button(
        "Generate",
        disabled=bytes_data is None or "api_key" not in st.session_state,
        key="generate",
    )

    if button and bytes_data is not None:
        with st.spinner("Generating..."):
            generate(bytes_data, st.session_state.api_key, product_attributes)
            st.balloons()

    if "product_description" in st.session_state:
        st.text_area(
            "Product description:",
            st.session_state.product_description,
            height=400,
        )


st.set_page_config(page_title="Product Descriptions", page_icon="👕")
st.write("# 👕 Product Descriptions")
st.write("Upload an image and generate a product description.")
st.info(
    "This is a test of the OpenAI GPT-4V preview and is not intended for production use."
)
st.write("\n")

run()

show_code([generate, run])
