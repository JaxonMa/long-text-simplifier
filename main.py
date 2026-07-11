# -*- coding: utf-8 -*-

"""
main.py
This is the main entry point for the long text simplifier application.

Author: Jaxon Ma
Date: 2026-07-10
"""

from openai import OpenAI
from simplifier import get_env_settings, simplify


def main():
    base_url, api_key, model, is_loop_enabled = get_env_settings()
    client = OpenAI(api_key=api_key, base_url=base_url)
    
    while is_loop_enabled:
        text = input("Enter the text you want to simplify (or type 'exit' to quit): ")
        if text.lower() == 'exit':
            break
        
        simplified_text = simplify(client, model, text)
        
        if simplified_text:
            print("Simplified Text:")
            print(simplified_text + "\n")
        else:
            print("Failed to simplify the text. Please try again.\n")
            

if __name__ == "__main__":
    main()
