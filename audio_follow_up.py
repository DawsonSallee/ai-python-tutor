# audio_follow_up.py (NEW, GENERIC VERSION)

import streamlit as st
import google.generativeai as genai
import io
import time

# --- This is the new, simple callback function. It is FAST. ---
def set_process_audio_flag():
    """
    This callback's ONLY job is to set a flag in session_state, indicating
    that there is new audio data ready to be processed.
    """
    audio_key = f"audio_recorder_{st.session_state.get('quiz_count', 0)}"
    if st.session_state[audio_key] is not None:
        st.session_state.process_audio_flag = True

def audio_follow_up_component():
    """Renders the audio input and handles the processing flow via a state flag."""

    # Initialize the flag if it doesn't exist
    if "process_audio_flag" not in st.session_state:
        st.session_state.process_audio_flag = False
    
    # --- UI Elements are now generic (no .sidebar) ---
    st.subheader("🗣️ Ask a Follow-up") # Using subheader is better for a column
    
    if "chat_session" in st.session_state:
        audio_key = f"audio_recorder_{st.session_state.get('quiz_count', 0)}"
        
        st.audio_input( # <-- NO .sidebar
            "Record a question about the content to send to Gemini:",
            key=audio_key,
            on_change=set_process_audio_flag
        )
    else:
        st.caption("Generate a quiz to enable follow-up questions.") # <-- NO .sidebar

    # --- Processing Logic (This part is unchanged) ---
    if st.session_state.process_audio_flag:
        st.session_state.process_audio_flag = False
        
        api_key = st.session_state.get("api_key")
        chat_session = st.session_state.get("chat_session")
        audio_bytes_data = st.session_state.get(f"audio_recorder_{st.session_state.get('quiz_count', 0)}")

        if api_key and chat_session and audio_bytes_data:
            with st.spinner("The Sage is thinking..."):
                try:
                    raw_audio_bytes = audio_bytes_data.getvalue()
                    audio_part = {"mime_type": "audio/wav", "data": raw_audio_bytes}
                    
                    follow_up_prompt = [
                        "You are an expert Python tutor. A user is asking a follow-up question about the previous quiz content. "
                        "Listen to their spoken question and provide a direct, clear, and concise answer. "
                        "Base your answer primarily on the context provided. If the information requested is not present in the given context, you may then draw upon your general knowledge."
                        "Keep your entire response under 150 words.",
                        audio_part
                    ]
                    
                    response = chat_session.send_message(follow_up_prompt)
                    st.session_state.follow_up_response = response.text

                except Exception as e:
                    st.session_state.follow_up_response = f"**An error occurred:**\n```\n{e}\n```"
            
            st.rerun()