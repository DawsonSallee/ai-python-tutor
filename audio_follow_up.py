# audio_follow_up.py (Corrected with Process-Once-and-Clear Pattern)

import streamlit as st
import google.generativeai as genai
import io
import time

def audio_follow_up_component():
    """
    Renders the audio input in the sidebar and handles the follow-up logic.
    The response is stored in session_state for the main app to display.
    This version ensures the audio is only processed once.
    """
    st.sidebar.divider()
    st.sidebar.header("🗣️ Ask a Follow-up")
    
    # We need a unique key that we can manually reset
    audio_key = f"audio_input_{st.session_state.get('quiz_count', 0)}"
    
    # Only show the audio input if a quiz has been generated
    if "chat_session" in st.session_state:
        audio_bytes = st.sidebar.audio_input(
            "Record a question about the quiz:",
            key=audio_key
        )
        
        # This block now only executes when there's NEW audio data
        if audio_bytes:
            api_key = st.session_state.get("api_key")
            chat_session = st.session_state.get("chat_session")

            if not api_key or not chat_session:
                st.sidebar.warning("Please enter your API key and generate a quiz first.")
                return

            with st.spinner("The Sage is thinking about your question..."):
                # ... (inside audio_follow_up_component function) ...
                try:
                    raw_audio_bytes = audio_bytes.getvalue()
                    audio_part = {"mime_type": "audio/wav", "data": raw_audio_bytes}
                    
                    # --- THIS IS THE SPECIFIC CHANGE ---
                    # We construct a multi-part message that includes a new instruction
                    # for this specific turn in the conversation.
                    
                    follow_up_prompt = [
                        "You are an expert Python tutor. A user is asking a follow-up question about the previous quiz content. "
                        "Listen to their spoken question and provide a direct, clear, and concise answer. "
                        "Base your answer ONLY on the context from the initial quiz. "
                        "Keep your entire response under 150 words.",
                        audio_part
                    ]
                    
                    # Send the combined prompt and audio to the existing chat session
                    response = chat_session.send_message(follow_up_prompt)
                    # ------------------------------------
                    
                    st.session_state.follow_up_response = response.text

                except Exception as e:
                    st.session_state.follow_up_response = f"**An error occurred:**\n```\n{e}\n```"
                finally:
                    # This block is GUARANTEED to run, even if an error occurs.
                    # This ensures the widget is always cleared.
                    st.session_state[audio_key] = None
                    st.rerun()
    else:
        st.sidebar.caption("Generate a quiz to enable follow-up questions.")