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
                try:
                    raw_audio_bytes = audio_bytes.getvalue()
                    audio_part = {"mime_type": "audio/wav", "data": raw_audio_bytes}
                    
                    response = chat_session.send_message(["Your spoken question is:", audio_part])
                    
                    st.session_state.follow_up_response = response.text

                except Exception as e:
                    st.session_state.follow_up_response = f"**An error occurred:**\n```\n{e}\n```"
            
            # === THE CRUCIAL FIX ===
            # After processing, we immediately clear the widget's state
            # by setting its key in session_state to None.
            st.session_state[audio_key] = None
            # =======================

            # Rerun to display the new response and show the cleared audio widget
            st.rerun()
    else:
        st.sidebar.caption("Generate a quiz to enable follow-up questions.")