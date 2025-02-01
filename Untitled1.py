import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv('untitled.env')

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon=":brain:",  # Favicon emoji
    layout="centered",  # Page layout option
)

# Retrieve API key from environment variables
GOOGLE_API_KEY = os.getenv("Gemini_API_KEY")
if not GOOGLE_API_KEY:
    st.error("API key not found! Please check your environment settings.")
    st.stop()

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('learnlm-1.5-pro-experimental')


# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role


# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
    st.session_state.chat_session.history.append({"role": "model", "parts": [{"text": "Hello! How are you?"}]})

# Sidebar with a reset chat button
with st.sidebar:
    st.title("Settings")
    if st.button("Reset Chat"):
        st.session_state.chat_session = model.start_chat(history=[])
        st.session_state.chat_session.history.append({"role": "model", "parts": [{"text": "Hello! How are you?"}]})
        st.experimental_rerun()

# Display the chatbot's title on the page
st.title("🤖 Gemini Pro - ChatBot")

# Display chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message["role"])):
        st.markdown(message["parts"][0]["text"])

# Input field for user's message
user_prompt = st.chat_input("Ask me...")
if user_prompt:
    st.chat_message("user").markdown(user_prompt)

    try:
        # Ensure the question is about Python libraries
        if "python" not in user_prompt.lower() and "library" not in user_prompt.lower():
            response_text = "I can only answer questions related to Python libraries. Please ask something relevant."
        else:
            # Send user's message to Gemini-Pro and get the response
            gemini_response = st.session_state.chat_session.send_message(user_prompt)
            response_text = gemini_response.text

        # Display response
        with st.chat_message("assistant"):
            st.markdown(response_text)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
