import os
import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu
from utils import load_gemini_pro_model, gemini_pro_vision_response

working_directory = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="Gemini AI",
    page_icon="*",
    layout="centered"
)


def translate_role(role):
    if role == 'model':
        return 'assistant'
    else:
        return role


with st.sidebar:
    choice = option_menu("Gemini AI", ["ChatBot", "Image Captioning", "Embed text", "Ask me anything"],
                         menu_icon='robot', icons=["", "", "", ""], default_index=0)

if choice == 'ChatBot':
    model = load_gemini_pro_model()

    st.title("ChatBot")
    if 'chat_session' not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    for history in st.session_state.chat_session.history:
        with st.chat_message(translate_role(history.role)):
            st.markdown(history.parts[0].text)

    prompt = st.chat_input("Start typing")
    if prompt:
        st.chat_message('user').markdown(prompt)

        response = st.session_state.chat_session.send_message(prompt)

        with st.chat_message('assistant'):
            st.markdown(response.text)

if choice == 'Image Captioning':
    st.title("Image Captioning")

    upload_image = st.file_uploader("Upload an image", type=['jpg', 'jpeg', 'png'])

    if st.button("Generate Caption"):
        image = Image.open(upload_image)

        col1, col2 = st.columns(2)

        with col1:
            resize_image = image.resize(512, 512)
            st.image(resize_image)

        default_prompt = "Give a short description of this image"

        caption = gemini_pro_vision_response(default_prompt, image)

        with col2:
            st.info(caption)





