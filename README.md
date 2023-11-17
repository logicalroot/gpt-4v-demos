# GPT-4V Testing Ground

[![Python 3.8+](https://img.shields.io/badge/Python%20-3.8%2B-orange)](https://www.python.org/downloads/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://gpt-4v-test.streamlit.app/)

This app provides some basic demos to test the vision capabilities of GPT-4V.

## Demos

<table>
  <tr><td>👕 Product Descriptions</td><td>Upload an image and generate a product description.</td></tr>
  <tr><td>📷 Camera</td><td>Take a photo with your device's camera and generate a caption.</td></tr>
  <tr><td>🧾 OCR</td><td>Upload an image and extract the text.</td></tr>
  <tr><td>📋 Quality Control</td><td>Upload an image and generate a QC report.</td></tr>
</table>

And more coming soon!

## Prerequisites

- Python 3.8+
- OpenAI API key

## Usage

1. Clone this repository.
2. Install the necessary packages:
```
pip install streamlit
```
3. Run the application:
```
streamlit run 🏠_Home.py
```
To remove the missing secrets warning, create a blank `secrets.toml` file in your `.streamlit` folder.

## OpenAI API key

To avoid inputting your OpenAI API key every run, you can add it to `secrets.toml` with the following line. Paste your key between the double quotes.
```
OPENAI_API_KEY = "YOUR KEY"
```
For safety, the filepath should be in your `.gitignore` file.

## Contributing

Feel free to build and share new demos using the code!

## About GPT-4V

- [OpenAI announcement](https://openai.com/blog/new-models-and-developer-products-announced-at-devday)
- [GPT-4V system card](https://openai.com/research/gpt-4v-system-card)

## License

This project is licensed under the terms of the MIT license.