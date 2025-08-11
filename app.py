import streamlit as st
from gtts import gTTS
import io
import random
import base64

# --- App Configuration ---
st.set_page_config(
    page_title="German Learning Buddy",
    page_icon="🇩🇪",
    layout="centered"
)

# A more extensive, hard-coded dictionary of common German words for the game.
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
if "german_word" not in st.session_state:
    st.session_state.german_word = None
    st.session_state.english_translation = None
    st.session_state.show_translation = False
    st.session_state.audio_played = False

def get_new_word_pair():
    """Selects a new random word and stores it in session state."""
    st.session_state.german_word, st.session_state.english_translation = random.choice(list(GERMAN_WORDS.items()))
    st.session_state.show_translation = False
    st.session_state.audio_played = False
    if 'user_guess' in st.session_state:
        del st.session_state.user_guess

def autoplay_audio():
    """Generates and autoplays the audio for the current German word."""
    if st.session_state.german_word and not st.session_state.audio_played:
        try:
            tts = gTTS(text=st.session_state.german_word, lang='de')
            audio_bytes_io = io.BytesIO()
            tts.write_to_fp(audio_bytes_io)
            audio_bytes_io.seek(0)
            
            # Encode the audio bytes to base64 for autoplay
            audio_base64 = base64.b64encode(audio_bytes_io.read()).decode('utf-8')
            audio_tag = f'''
            <audio autoplay>
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
            '''
            st.components.v1.html(audio_tag, height=0)
            st.session_state.audio_played = True
        except Exception as e:
            st.error(f"Failed to generate audio: {str(e)}")

# --- App UI & Logic ---
st.title("German Learning Buddy 🇩🇪")
st.markdown("---")

# Initialize the first word if the app just started
if st.session_state.german_word is None:
    get_new_word_pair()

# Display the German word and play audio automatically
st.header(st.session_state.german_word)
autoplay_audio()

# User input section
user_guess = st.text_input(
    "Type the German word/phrase exactly as shown (press Enter to submit):",
    key="user_guess",
    on_change=lambda: setattr(st.session_state, 'show_translation', True)
)

# Show translation when user submits (presses Enter)
if st.session_state.show_translation:
    st.markdown(f"**English translation:** {st.session_state.english_translation}")
    
    # Button to trigger next word (acts like pressing Enter again)
    if st.button("Next Word (or press Enter)"):
        get_new_word_pair()
        st.experimental_rerun()

# --- Footer ---
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit and gTTS")
