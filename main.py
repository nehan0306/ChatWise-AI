import os
import streamlit as st
from PIL import Image
import fitz
import pyttsx3
from streamlit_option_menu import option_menu
from utils import load_gemini_pro_model, gemini_pro_vision_response, gemini_pro_response

working_directory = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="ChatWise",
    page_icon="*",
    layout="centered"
)


def translate_role(role):
    if role == 'model':
        return 'assistant'
    else:
        return role


def text_to_voice(text):
    if text:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)

        engine.say(text)
        engine.runAndWait()


with st.sidebar:
    choice = option_menu("ChatWise AI", ["ChatBot", "PDF Summarizer", "Ask Me Anything", "Image Captioning"],
                         menu_icon='robot', icons=["chat-square-text", "file-pdf", "question-square", "image"], default_index=0)

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

        st.session_state.response = response.text

        with st.chat_message('assistant'):
            st.markdown(st.session_state.response)

if choice == 'Image Captioning':
    st.title("Image Captioning")

    upload_image = st.file_uploader("Upload an image", type=['jpg', 'jpeg', 'png'])

    if st.button("Generate Caption"):
        image = Image.open(upload_image)

        col1, col2 = st.columns(2)

        with col1:
            st.image(image)

        default_prompt = "Give a short description of this image"

        st.session_state.response = gemini_pro_vision_response(default_prompt, image)

        with col2:
            st.info(st.session_state.response)

if choice == 'PDF Summarizer':
    st.title("PDF Reader")

    upload_pdf = st.file_uploader("Upload a PDF", type=['pdf'])

    if st.button("Summarize PDF"):
        if upload_pdf is not None:
            pdf_text = ""
            with fitz.open(stream=upload_pdf.read(), filetype="pdf") as pdf_document:
                for page_number in range(len(pdf_document)):
                    page = pdf_document.load_page(page_number)
                    pdf_text += page.get_text()

            prompt = f"Summarize this text extracted from a PDF: {pdf_text}"

            st.session_state.response = gemini_pro_response(prompt)
            st.markdown(st.session_state.response)

if choice == 'Ask Me Anything':
    st.title("Ask me a question")

    prompt = st.text_area(label='Please enter a question', placeholder="Ask me anything")

    if st.button("Get response"):
        st.session_state.response = gemini_pro_response(prompt)
        st.markdown(st.session_state.response)

if st.sidebar.button("Read Text") and st.session_state.response:
    text_to_voice(st.session_state.response)
    if choice != "ChatBot":
        st.markdown(st.session_state.response)

