import os
import subprocess
from typing import List, Optional

import openai
from yaml import safe_load

import streamlit as st

CONFIG_FILE = 'config.yml'
OPENAI_TOKEN = "OPENAI_TOKEN"
OPENAI_ORG = "OPENAI_ORG"

MODEL = "gpt-3.5-turbo"  # Model to use

TEMP_MD_FILE = "__temp.md"
TEMP_PDF_FILE = "__temp.pdf"


def complete_text(prompt: str, previous_messages: Optional[List[str]] = None) -> str:
    """
    Complete text using GPT-3.5 Turbo
    :param prompt: Prompt to complete
    :param previous_messages: Previous messages
    :return: Completed text
    """
    if previous_messages is None:
        previous_messages = []

    messages = [{"role": "user", "content": prompt + " Markdown."}] + previous_messages

    return openai.ChatCompletion.create(model=MODEL, messages=messages)["choices"][0]["message"]["content"]


def create_exam(prompt: str):
    """
    Create exam using GPT-3.5 Turbo
    :param prompt: Prompt to complete
    """
    markdown = complete_text(prompt)

    with open(TEMP_MD_FILE, "w") as f:
        f.write(markdown)

    subprocess.run([
        "mdpdf", TEMP_MD_FILE,
        "--output", TEMP_PDF_FILE,
        "--footer", ",,{page}",
        "--paper", "A4"
    ])

    os.remove(TEMP_MD_FILE)


def initial_config():
    """
    Initial configuration of OpenAI API
    """
    config = safe_load(open(CONFIG_FILE))
    openai.organization = config[OPENAI_ORG]
    openai.api_key = config[OPENAI_TOKEN]


def main():
    initial_config()

    st.title("Exam generator")

    prompt = st.text_area("Prompt", placeholder="Write a prompt to describe the exam that you want.")

    if st.button("Generate"):
        st.warning("This can take a while...")
        create_exam(prompt)
        contents = open(TEMP_PDF_FILE, "rb").read()
        st.download_button("Download PDF", contents, "exam.pdf", "application/pdf")


if __name__ == '__main__':
    main()
