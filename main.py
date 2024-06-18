import os
import streamlit as st
from streamlit_option_menu import option_menu
from utils import load_gemini_pro_model

working_directory = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="Gemini AI",
    page_icon="*",
    layout="centered"
)


with st.sidebar:
    selected = option_menu("Gemini AI", ["ChatBot", "Image Capturing", "Embed text", "Ask me anything"],
                           menu_icon='robot', icons=["", "", "", ""], default_index=0)



