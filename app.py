import streamlit as st
import random
import pyttsx3
import tempfile
import os

# ----------------------------
# Word list
# ----------------------------
words = {
    "Hund": "dog",
    "Katze": "cat",
    "Haus": "house",
    "Buch": "book",
    "Auto": "car",
    "Baum": "tree",
    "Stuhl": "chair",
    "Tisch": "table",
    "Wasser": "water",
    "Brot": "bread",
    "Apfel": "apple",
    "Milch": "milk",
    "Schule": "school",
    "Fenster": "window",
    "Tür": "door",
    "Sonne": "sun",
    "Mond": "moon",
    "Stern": "star",
    "Himmel": "sky",
    "Erde": "earth",
    "rot": "red",
    "blau": "blue",
    "grün": "green",
    "heiß": "hot",
    "kalt": "cold",
    "groß": "big",
    "klein": "small",
    "schön": "beautiful",
    "hässlich": "ugly",
    "alt": "old",
    "jung": "young",
    "neu": "new",
    "schnell": "fast",
    "langsam": "slow",
    "glücklich": "happy",
    "traurig": "sad",
    "müde": "tired",
    "hungrig": "hungry"
}

# ----------------------------
# Text-to-speech initialization
# ----------------------------

@st.cache_resource
def get_tts_engine():
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)  # Adjust speed
    engine.setProperty("volume", 1.0)
    voices = engine.getProperty("voices")
    # Try to find a German voice
    for voice in voices:
        if "german" in voice.name.lower() or "deutsch" in voice.name.lower():
            engine.setProperty("voice", voice.id)
            break
    return engine

def speak_text(text):
    """Convert text to speech and return audio file path"""
    engine = get_tts_engine()
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tmp_path = tmp_file.name
    tmp_file.close()
    engine.save_to_file(text, tmp_path)
    engine.runAndWait()
    return tmp_path

# ----------------------------
# Streamlit App
# ----------------------------
st.set_page_config(page_title="Learn German", page_icon="🇩🇪")
st.title("🇩🇪 Learn German Vocabulary")

if "current_word" not in st.session_state:
    st.session_state.current_word = random.choice(list(words.keys()))
    st.session_state.show_translation = False

# Current word display
word = st.session_state.current_word
st.subheader(f"German word: **{word}**")

# Play audio
if st.button("🔊 Hear pronunciation"):
    audio_file = speak_text(word)
    audio_bytes = open(audio_file, "rb").read()
    st.audio(audio_bytes, format="audio/mp3")
    os.remove(audio_file)

# Show / hide translation
if st.button("Show Translation"):
    st.session_state.show_translation = True

if st.session_state.show_translation:
    st.write(f"**English:** {words[word]}")

# Next word button
if st.button("Next Word"):
    st.session_state.current_word = random.choice(list(words.keys()))
    st.session_state.show_translation = False
