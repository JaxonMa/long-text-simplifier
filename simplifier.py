# -*- coding: utf-8 -*-

"""
simplifier.py
This file contains functions that requests a certain API for long text simplifying.

Author: Jaxon Ma
Date: 2026-07-10
"""

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
BASE_URL = os.getenv("BASE_URL", "URL_TO_API")
API_KEY = os.getenv("API_KEY", "YOUR_API_KEY")
MODEL = os.getenv("MODEL", "MODEL_NAME")
RUN_CONTINUOUSLY = os.getenv("RUN_CONTINUOUSLY", "True").lower() == "true"
CLIENT = OpenAI(api_key=API_KEY, base_url=BASE_URL)


def get_prompt() -> str:
    with open("prompt.md", "r") as file:
        return file.read()
    return "Please simplify the following text while maintaining its original meaning and context. " \
            + "Ensure that the simplified version is clear, concise, and easy to understand. " \
            + "Use the language user's input is in, and avoid changing the tone or style of the text. "


def simplify(text: str) -> str | None:
    """
    Simplifies the given text using the OpenAI API.

    Args:
        text (str): The text to be simplified.

    Returns:
        str | None: The simplified text if successful, None otherwise.
    """
    try:
        response = CLIENT.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": get_prompt()},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error simplifying text: {e}")
        return None


def main():
    with open("sample_text.txt", "r") as file:
        text = file.read()
    simplified_text = simplify(text)
    if simplified_text:
        print("Simplified Text:")
        print(simplified_text)
        

if __name__ == "__main__":
    main()
