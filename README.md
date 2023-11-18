# GPT-4V Demos

[![Python 3.8+](https://img.shields.io/badge/Python%20-3.8%2B-orange)](https://www.python.org/downloads/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://gpt-4v-test.streamlit.app/)

This mobile-friendly web app provides some basic demos to test the vision capabilities of GPT-4V.

[Streamlit](https://streamlit.io) was selected as a framework for this project to enable rapid prototyping of new ideas.

## Examples

<table>
  <tr><td>👕 Product Descriptions</td><td>Upload an image and generate a product description.</td></tr>
  <tr>
    <td width="30%">
      <img src="test_images/pre-generated_hoodie.png" width="100%" alt="Pre-generated Hoodie" /><br />
      <code style="font-size: 10px;">{ "product_attributes": { "brand_name": "Logical Root", "product_name": "Pre-generated Hoodie", "materials": "100% digital cotton" } }</code>
    </td>
    <td>
      <code style="font-size: 10px;">{ "description": "Embrace the fusion of art and comfort with the Logical Root Pre-generated Hoodie, a masterpiece crafted from 100% digital cotton to provide unparalleled softness and durability. The hoodie comes in a classic, versatile shade of black, boasting a bold graphic print at its core that captures a whirlwind of vibrant colors in an abstract design, promising to turn heads and spark conversations. With a spacious front pocket to keep your essentials close and a snug hoodie with adjustable drawstrings for those extra chilly days, this piece is the epitome of functional fashion. The ribbed cuffs and hem ensure a perfect fit while adding to the overall sleek silhouette, making it a must-have addition to your wardrobe whether you're aiming for a casual day out or a statement-making ensemble." }</code>
    </td>
  </tr>
  <tr><td>📷 Camera</td><td>Take a photo with your device's camera and generate a caption.</td></tr>
  <tr><td>🧾 OCR</td><td>Upload an image and extract the text.</td></tr>
  <tr><td>📋 Quality Control</td><td>Upload an image and generate a QC report.</td></tr>
</table>

And more coming soon!

## Prerequisites

- Python 3.8+
- OpenAI API key
> [How can I access GPT-4?](https://help.openai.com/en/articles/7102672-how-can-i-access-gpt-4)

## Local setup

Here's how you can get started.

1. Clone this repository.
```
git clone https://github.com/logicalroot/gpt-4v-demos.git
cd gpt-4v-demos
```
2. Install the necessary packages:
```
pip install streamlit
```
3. Run the application:
```
streamlit run 🏠_Home.py
```
4. To remove the missing secrets warning, create a blank `secrets.toml` file in your `.streamlit` folder.

> [!TIP]
> To avoid inputting your OpenAI API key every run, you can add it to `secrets.toml` with the following line. Paste your key between the double quotes.
> ```
> OPENAI_API_KEY = "YOUR KEY"
> ```
> For safety, ensure the filepath is in your `.gitignore` file.

## Contributing

Feel free to build and share new demos using the code!

## About GPT-4V

- [OpenAI announcement](https://openai.com/blog/new-models-and-developer-products-announced-at-devday)
- [GPT-4V system card](https://openai.com/research/gpt-4v-system-card)

## License

This project is licensed under the terms of the MIT license.