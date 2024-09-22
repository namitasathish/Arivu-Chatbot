import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
from google.generativeai.types import StopCandidateException
import time  

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("Google API Key not found. Please check your .env file.")
else:
    gen_ai.configure(api_key=GOOGLE_API_KEY)
    model = gen_ai.GenerativeModel('gemini-pro')

    st.set_page_config(
        page_title="Arivu",
        layout="centered",
    )
    st.markdown("""
        <style>
            header {
                border-top: 55px solid transparent; 
                padding-bottom: 50px;
            }
            .user-message {
                display: flex;
                justify-content: flex-end; 
                margin-bottom: 10px;
            }
            .user-message .message-text {
                background-color: #1b263b; 
                padding: 10px;
                border-radius: 15px;
                max-width: 60%;
                word-wrap: break-word;
            }
            .assistant-message {
                display: flex;
                justify-content: flex-start;
                margin-bottom: 10px;
            }
            .assistant-message .message-text {
                background-color: #415a77;
                padding: 10px;
                border-radius: 15px;
                max-width: 60%;
                word-wrap: break-word;
            }
            /* Loader animation */
            .loading-container {
                display: flex;
                justify-content: flex-start;
                margin-bottom: 10px;
                margin-left: 10px;
            }
            .loading-strips {
                width: 5px;
                height: 25px;
                margin: 0 2px;
                background-color: #dc2f02;
                animation: growShrink 1s infinite;
            }
            .loading-strips:nth-child(2) {
                background-color: #e85d04;
                animation-delay: 0.1s;
            }
            .loading-strips:nth-child(3) {
                background-color: #f48c06;
                animation-delay: 0.2s;
            }
            @keyframes growShrink {
                0%, 100% {
                    transform: scaleY(1);
                }
                50% {
                    transform: scaleY(1.5);
                }
            }
        
            
        </style>
    """, unsafe_allow_html=True)

    def translate_role_for_streamlit(user_role):
        return "assistant" if user_role == "model" else user_role

    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    st.title("Arivu - Your Chatbot")

    if len(st.session_state.chat_session.history) == 0:
        st.markdown("<p style='font-size: 15px; color: #555;'>Welcome to Arivu! You can start by asking questions like:<br/><i>‘What can you do?’, ‘Tell me a joke!’, ‘Help me with a topic’</i> <br/>WebDesign by NAMITASATHISH</p>", unsafe_allow_html=True)
 
    for message in st.session_state.chat_session.history:
        role = translate_role_for_streamlit(message.role)
        if role == "assistant":
            st.markdown(f'<div class="assistant-message"><div class="message-text">{message.parts[0].text}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="user-message"><div class="message-text">{message.parts[0].text}</div></div>', unsafe_allow_html=True)

    user_prompt = st.chat_input("Ask Arivu....")
    if user_prompt:
        st.markdown(f'<div class="user-message"><div class="message-text">{user_prompt}</div></div>', unsafe_allow_html=True)

  
        loader = st.markdown("""
            <div class="loading-container">
                <div class="loading-strips"></div>
                <div class="loading-strips"></div>
                <div class="loading-strips"></div>
            </div>
        """, unsafe_allow_html=True)

        try:
            time.sleep(2) 
            gemini_response = st.session_state.chat_session.send_message(user_prompt)
            loader.empty()

            st.markdown(f'<div class="assistant-message"><div class="message-text">{gemini_response.text}</div></div>', unsafe_allow_html=True)

        except StopCandidateException as e:
            loader.empty()
            st.error("Oops! Something went wrong with the response. Please try again.")
            st.write(f"Error Details: {e}")

