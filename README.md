# GPT-4V Testing Ground

[![Python 3.8+](https://img.shields.io/badge/Python%20-3.8%2B-orange)](https://www.python.org/downloads/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://gpt-4v-test.streamlit.app/)

This app provides some basic demos to test the vision capabilities of GPT-4.

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

## OpenAI API key

To remove the missing secrets warning, create a blank `secrets.toml` file in your `.streamlit` directory.

If you don't want to input your OpenAI API key in the sidebar every run, you can add it to `secrets.toml` with following line:
```
OPENAI_API_KEY = "YOUR KEY"
```
Make sure you add `secrets.toml` to your `.gitignore` file to keep the key safe.

## About GPT-4V

- [OpenAI announcement](https://openai.com/blog/new-models-and-developer-products-announced-at-devday)
- [GPT-4V system card](https://openai.com/research/gpt-4v-system-card)

## License

This project is licensed under the terms of the MIT license.