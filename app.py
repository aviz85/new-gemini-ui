import os
import streamlit as st
import google.generativeai as genai
from streamlit_chat import message
import toml

# Load config
config = toml.load('.streamlit/secrets.toml')
genai.configure(api_key=config['GEMINI_API_KEY'])

# Initialize chat model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-exp-1121",
    generation_config=generation_config,
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat = model.start_chat()
else:
    # Recreate chat with full history when page reloads
    history = [
        {"role": msg["role"], "parts": [msg["content"]]} 
        for msg in st.session_state.messages
    ]
    st.session_state.chat = model.start_chat(history=history)

st.title("Gemini Chat Bot")

# Chat input
user_input = st.text_input("הקלד הודעה:", key="user_input")

if user_input:
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Get bot response
    response = st.session_state.chat.send_message(user_input)
    st.session_state.messages.append({"role": "assistant", "content": response.text})

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        message(msg["content"], is_user=True)
    else:
        message(msg["content"]) 