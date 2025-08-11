import streamlit as st
import random
import edge_tts
import asyncio
import tempfile
import os

# --- German words dictionary ---
GERMAN_WORDS = {
    "Hallo": "Hello",
    "Danke": "Thank you",
    "Bitte": "Please",
    "Ja": "Yes",
    "Nein": "No",
    "Entschuldigung": "Excuse me",
    "Guten Morgen": "Good morning",
    "Guten Tag": "Good day",
    "Guten Abend": "Good evening",
    "Auf Wiedersehen": "Goodbye",
    "Wie geht es Ihnen?": "How are you? (formal)",
    "Wie geht's?": "How are you? (informal)",
    "Mir geht es gut": "I am fine",
    "Ich heiße": "My name is",
    "Was ist das?": "What is that?",
    "Ich verstehe nicht": "I don't understand",
    "Sprechen Sie Englisch?": "Do you speak English?",
    "die Katze": "the cat",
    "der Hund": "the dog",
    "das Buch": "the book",
    "das Auto": "the car",
    "der Mann": "the man",
    "die Frau": "the woman",
    "das Kind": "the child",
    "das Haus": "the house",
    "die Schule": "the school",
    "das Essen": "the food",
    "das Wasser": "the water",
    "die Milch": "the milk",
    "der Kaffee": "the coffee",
    "der Tee": "the tea",
    "das Brot": "the bread",
    "der Apfel": "the apple",
    "die Banane": "the banana",
    # Add more if you want
}

# --- Async helper to generate TTS audio with edge-tts ---
async def generate_tts_audio(text: str, voice: str = "de-DE-KatjaNeural"):
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    communicator = edge_tts.Communicate(text, voice)
    await communicator.save(tmp_file.name)
    return tmp_file.name

def get_audio_file(text):
    return asyncio.run(generate_tts_audio(text))

# --- Streamlit app ---
st.set_page_config(page_title="German Learning Buddy", page_icon="🇩🇪")

st.title("German Learning Buddy 🇩🇪")
st.write("Welcome to your German vocabulary trainer!")
st.markdown("---")

if "german_word" not in st.session_state:
    st.session_state.german_word, st.session_state.english_translation = random.choice(list(GERMAN_WORDS.items()))
    st.session_state.show_translation = False

st.header(st.session_state.german_word)

if st.button("🔊 Hear pronunciation"):
    try:
        audio_path = get_audio_file(st.session_state.german_word)
        audio_bytes = open(audio_path, "rb").read()
        st.audio(audio_bytes, format="audio/mp3")
        os.remove(audio_path)
    except Exception as e:
        st.error(f"Audio generation failed: {e}")

if not st.session_state.show_translation:
    with st.form("guess_form"):
        _ = st.text_input("Type the German word here:")
        submitted = st.form_submit_button("Submit")
    if submitted:
        st.session_state.show_translation = True
else:
    st.markdown("### Translation:")
    st.write(st.session_state.english_translation)
    with st.form("next_form"):
        _ = st.text_input("Press Enter for next word:", value="")
        next_submitted = st.form_submit_button("Next")
    if next_submitted:
        st.session_state.german_word, st.session_state.english_translation = random.choice(list(GERMAN_WORDS.items()))
        st.session_state.show_translation = False
        st.experimental_rerun()

st.markdown("---")
st.caption("Made with ❤️ using Streamlit and edge-tts")
