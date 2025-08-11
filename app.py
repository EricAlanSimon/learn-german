# app.py

import streamlit as st
from gtts import gTTS
import os
import io
import random

# --- App Configuration ---
st.set_page_config(
    page_title="German Learning Buddy",
    page_icon="🇩🇪",
    layout="centered"
)

# A more extensive, hard-coded dictionary of common German words for the game.
# This list contains more than 100 common words.
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
    "die Straße": "the street",
    "die Stadt": "the city",
    "das Land": "the country",
    "der Baum": "the tree",
    "die Blume": "the flower",
    "die Sonne": "the sun",
    "der Mond": "the moon",
    "der Stern": "the star",
    "die Wolke": "the cloud",
    "der Himmel": "the sky",
    "der Freund": "the friend (male)",
    "die Freundin": "the friend (female)",
    "die Familie": "the family",
    "der Vater": "the father",
    "die Mutter": "the mother",
    "der Bruder": "the brother",
    "die Schwester": "the sister",
    "die Liebe": "the love",
    "das Glück": "the happiness",
    "die Zeit": "the time",
    "das Geld": "the money",
    "der Schlüssel": "the key",
    "die Tür": "the door",
    "das Fenster": "the window",
    "die Lampe": "the lamp",
    "der Tisch": "the table",
    "der Stuhl": "the chair",
    "das Bett": "the bed",
    "der Computer": "the computer",
    "das Telefon": "the phone",
    "der Tag": "the day",
    "die Nacht": "the night",
    "die Woche": "the week",
    "der Monat": "the month",
    "das Jahr": "the year",
    "der Sommer": "the summer",
    "der Winter": "the winter",
    "der Herbst": "the autumn",
    "der Frühling": "the spring",
    "heute": "today",
    "morgen": "tomorrow",
    "gestern": "yesterday",
    "jetzt": "now",
    "später": "later",
    "früher": "earlier",
    "oben": "up",
    "unten": "down",
    "links": "left",
    "rechts": "right",
    "hier": "here",
    "dort": "there",
    "schön": "beautiful",
    "gut": "good",
    "schlecht": "bad",
    "groß": "big",
    "klein": "small",
    "alt": "old",
    "neu": "new",
    "jung": "young",
    "schnell": "fast",
    "langsam": "slow",
    "heiß": "hot",
    "kalt": "cold",
    "hell": "bright",
    "dunkel": "dark",
    "leicht": "easy / light",
    "schwer": "difficult / heavy",
    "frei": "free",
    "voll": "full",
    "leer": "empty",
    "bereit": "ready",
    "krank": "sick",
    "gesund": "healthy",
    "traurig": "sad",
    "glücklich": "happy",
    "müde": "tired",
    "durstig": "thirsty",
    "hungrig": "hungry"
}


# --- State Initialization ---
# This is crucial for Streamlit to remember the state between re-runs
if "german_word" not in st.session_state:
    st.session_state.german_word = None
    st.session_state.english_translation = None
    st.session_state.show_translation = False
    st.session_state.feedback = ""

def get_new_word_pair():
    """Selects a new random word and stores it in session state."""
    st.session_state.show_translation = False
    st.session_state.feedback = ""
    st.session_state.german_word, st.session_state.english_translation = random.choice(list(GERMAN_WORDS.items()))
    # To clear the input box for the next round
    if 'user_guess' in st.session_state:
        del st.session_state.user_guess

def play_audio():
    """Generates and plays the audio for the current German word."""
    if st.session_state.german_word:
        try:
            tts = gTTS(text=st.session_state.german_word, lang='de')
            audio_bytes_io = io.BytesIO()
            tts.write_to_fp(audio_bytes_io)
            audio_bytes_io.seek(0)
            st.audio(audio_bytes_io, format="audio/mp3")
        except Exception as e:
            st.error(f"Failed to generate audio. Please check your network connection.")
            st.warning("This is likely a temporary issue with the text-to-speech service.")

# --- App UI & Logic ---

st.title("German Learning Buddy 🇩🇪")
st.markdown("---")
st.write("Welcome to your German vocabulary trainer!")

# Initialize the first word if the app just started
if st.session_state.german_word is None:
    get_new_word_pair()

# Display the German word to be repeated
st.header(st.session_state.german_word)

# Play audio for the German word
if st.button("🔊 Play Pronunciation"):
    play_audio()

# --- User Guess Section ---
user_guess = st.text_input("Type the German word here:", key="user_guess")

# Handle the user's guess and provide feedback
if st.button("Check Answer"):
    if user_guess.strip().lower() == st.session_state.german_word.lower():
        st.session_state.feedback = f"✅ Correct! The English translation is '{st.session_state.english_translation}'."
        st.session_state.show_translation = True
    else:
        st.session_state.feedback = "❌ Incorrect. Try again!"
        st.session_state.show_translation = False

# Display feedback and the correct answer if requested
if st.session_state.feedback:
    st.markdown("### Feedback:")
    if st.session_state.feedback.startswith("✅"):
        st.success(st.session_state.feedback)
        st.session_state.show_translation = True
    else:
        st.error(st.session_state.feedback)

# Show a new word button
if st.session_state.show_translation:
    if st.button("Get a New Word"):
        get_new_word_pair()

# --- Footer ---
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit and gTTS")
