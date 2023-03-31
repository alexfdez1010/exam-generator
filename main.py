import os
import subprocess

import openai
import streamlit as st

from app.app import get_app
from utils.api import complete_text

OPENAI_TOKEN = "OPENAI_TOKEN"
OPENAI_ORG = "OPENAI_ORG"  # Model to use

def create_exam(prompt: str):
    """
    Create exam using GPT-3.5 Turbo
    :param prompt: Prompt to complete
    """
    markdown = complete_text(prompt)




def initial_config():
    """
    Initial configuration of OpenAI API and streamlit
    """
    openai.organization = st.secrets[OPENAI_ORG]
    openai.api_key = st.secrets[OPENAI_TOKEN]

    st.set_page_config(
        page_title="Exam generator",
        page_icon=":pencil2:",
        layout="wide",
        initial_sidebar_state="expanded"
    )


def main():
    initial_config()

    app = get_app()
    app.render()


if __name__ == '__main__':
    main()
