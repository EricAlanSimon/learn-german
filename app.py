# app.py

import streamlit as st
from gtts import gTTS
import os
import io

# --- App Configuration ---
st.set_page_config(
    page_title="German Learning Buddy",
    page_icon="🇩🇪",
    layout="centered"
)

# --- App UI & Logic ---

st.title("German Learning Buddy 🇩🇪")
st.markdown("---")

st.write("Enter a German word or phrase below to get its translation and hear the pronunciation.")

# A simple, hard-coded dictionary for demonstration purposes.
# For a real application, you might use a more comprehensive API or a large dataset.
german_to_english_dictionary = {
    "Hallo": "Hello",
    "Guten Tag": "Good day",
    "Wie geht es Ihnen?": "How are you? (formal)",
    "Ich bin gut": "I am well",
    "Danke": "Thank you",
    "Bitte": "Please / You're welcome",
    "Tschüss": "Bye",
    "Ja": "Yes",
    "Nein": "No"
}

# --- User Input Section ---
user_input = st.text_input("Enter German text here:", value="Hallo")

# --- Translation and Audio Section ---
if st.button("Translate & Pronounce"):
    if user_input:
        # Check if the word is in our simple dictionary
        translation = german_to_english_dictionary.get(user_input.strip(), "Translation not found.")
        
        st.write(f"### Translation:")
        st.info(translation)

        st.write("### Pronunciation:")
        
        try:
            # Generate the audio from the German text
            tts = gTTS(text=user_input, lang='de')
            
            # Save the audio to a BytesIO object instead of a file
            audio_bytes_io = io.BytesIO()
            tts.write_to_fp(audio_bytes_io)
            audio_bytes_io.seek(0)
            
            # Use Streamlit's audio player
            st.audio(audio_bytes_io, format="audio/mp3")

        except Exception as e:
            st.error(f"An error occurred while generating audio: {e}")
            st.warning("Please check your internet connection or try a different phrase.")
    else:
        st.warning("Please enter some text to translate and pronounce.")

# --- Footer ---
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit and gTTS")
