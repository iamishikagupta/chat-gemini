import streamlit as st
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

def get_api_key():
    return os.getenv("API_KEY")

def login(username, password):
    if username == "chat" and password == "0000":
        return True
    return False

def main():
    st.set_page_config(page_title="LLM Chatgpt With Gemini", layout="wide")

    # Apply custom CSS for text input width
    st.markdown(
        """
        <style>
        .stTextInput {
            width: 300px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.title("Login Page")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.button("Login")

        if login_button:
            if login(username, password):
                st.session_state.logged_in = True
                st.session_state.show_toast = True
                st.rerun()
            else:
                st.error("Invalid username or password")
    else:
        st.title("LLM chatbot with Gemini😉")
        st.caption("Chat with Gemini model using Image and text for lightning fast response")

        api_key = get_api_key()

        if api_key:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")
            st.success('You are Logged In')

            if "show_toast" in st.session_state and st.session_state.show_toast:
                st.toast('Now You can ask Questions freely')
                st.balloons()
                st.session_state.show_toast = False  # Reset the flag

            # Initialize chat history in session state
            if "message" not in st.session_state:
                st.session_state.message = []

            # Sidebar for image upload
            with st.sidebar:
                st.title("Chat with Images")
                uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])
                if uploaded_file:
                    image = Image.open(uploaded_file)
                    st.image(image, caption='Uploaded image', use_column_width=True)

            # Layout for chat history
            chat_placeholder = st.container()

            with chat_placeholder:
                for message in st.session_state.message:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

            # Input prompt
            prompt = st.chat_input("What do you want to know buddy😊")

            if prompt:
                inputs = [prompt]
                st.session_state.message.append({"role": "user", "content": prompt})
                with chat_placeholder:
                    with st.chat_message("user"):
                        st.markdown(prompt)

                if uploaded_file:
                    inputs.append(image)

                with st.spinner('Generating response... please wait'):
                    response = model.generate_content(inputs)

                with chat_placeholder:
                    with st.chat_message("assistant"):
                        st.markdown(response.text)

            if uploaded_file and not prompt:
                st.warning("Please enter a text query to accompany the image.")
        else:
            st.warning("Please enter your Google API key in the .env file.")

if __name__ == "__main__":
    main()
