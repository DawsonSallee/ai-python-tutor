# audio_follow_up.py (Final, Correct Version using on_change Callback)

import streamlit as st
import google.generativeai as genai
import io
import time

def process_audio_follow_up():
    """
    This function is called automatically when new audio is recorded.
    It handles the API call and stores the response in session state.
    """
    audio_key = f"audio_recorder_{st.session_state.get('quiz_count', 0)}"
    
    # Check if there's audio data in the state from the widget
    if audio_key in st.session_state and st.session_state[audio_key] is not None:
        audio_bytes_data = st.session_state[audio_key]
        
        api_key = st.session_state.get("api_key")
        chat_session = st.session_state.get("chat_session")

        if not api_key or not chat_session:
            st.sidebar.warning("API key and a generated quiz are required.")
            return

        with st.spinner("The Sage is thinking about your question..."):
            try:
                raw_audio_bytes = audio_bytes_data.getvalue()
                audio_part = {"mime_type": "audio/wav", "data": raw_audio_bytes}
                
                follow_up_prompt = [
                    "You are an expert Python tutor. A user is asking a follow-up question about the previous quiz content. "
                    "Listen to their spoken question and provide a direct, clear, and concise answer. "
                    "Base your answer ONLY on the context from the initial quiz. "
                    "Keep your entire response under 150 words.",
                    audio_part
                ]
                
                response = chat_session.send_message(follow_up_prompt)
                st.session_state.follow_up_response = response.text

            except Exception as e:
                st.session_state.follow_up_response = f"**An error occurred:**\n```\n{e}\n```"
        
        # We don't need to manually clear the state or rerun.
        # Streamlit handles the rerun after the callback finishes.

def audio_follow_up_component():
    """Renders the audio input widget in the sidebar."""
    st.sidebar.divider()
    st.sidebar.header("🗣️ Ask a Follow-up")
    
    if "chat_session" in st.session_state:
        # THE KEY CHANGE: We pass our function to the 'on_change' parameter.
        st.sidebar.audio_input(
            "Record a question about the quiz:",
            key=f"audio_recorder_{st.session_state.get('quiz_count', 0)}",
            on_change=process_audio_follow_up # <--- THIS IS THE FIX
        )
    else:
        st.sidebar.caption("Generate a quiz to enable follow-up questions.")