import streamlit as st
from gtts import gTTS
from openai import OpenAI
import os



client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(
    page_title="Translate Text",
    page_icon="🌐",
    layout="centered",
)

st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}
.title {
    font-size: 3rem;
    font-weight: 600;
    color: #2c3e50;
    text-align: center;
    margin-bottom: 1rem;
}
.subtitle {
    font-size: 1.2rem;
    color: #34495e;
    text-align: center;
    margin-bottom: 2rem;
}
.result-box {
    background-color: #ecf0f1;
    border-radius: 10px;
    padding: 1rem;
    font-size: 1.1rem;
    color: #2c3e50;
}
.stButton>button {
    background-color: #3498db;
    color: white;
    font-weight: bold;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-size: 1rem;
    transition: 0.3s;
}
.stButton>button:hover {
    background-color: #2980b9;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="title">Experience AI Translation 🌐</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="subtitle">Enter text and select language</div>',
    unsafe_allow_html=True
)

# Sidebar
with st.sidebar:
    st.header("Settings")

target_language = st.selectbox(
    "Select target language",
    ["French", "Spanish", "German", "Chinese", "Japanese", "Hindi","Urdu"]
)

target_display = st.selectbox(
    "Select output format",
    ["Text", "Audio"]
)

# Language map for speech
lang_map = {
    "Hindi": "hi",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Japanese": "ja",
    "Chinese": "zh-cn"
}

# Input
st.subheader("Enter text to translate")
input_text = st.text_area("Input Text", height=150)

# Button
if st.button("Translate"):

    if input_text.strip() == "":
        st.warning("Please enter text to translate.")

    else:
        with st.spinner("Translating..."):

            prompt = f"""
You are a professional translation system.

Translate the text below into {target_language}.

Rules:
- Output ONLY the translated text
- No explanations
- No extra words
- No greetings
- Keep meaning accurate and natural

Text:
{input_text}
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            translated_text = response.choices[0].message.content.strip()

        # OUTPUT SECTION
        if target_display == "Audio":
            tts = gTTS(
                translated_text,
                lang=lang_map[target_language]
            )
            audio_file = "translated_audio.mp3"
            tts.save(audio_file)
            st.audio(audio_file, format="audio/mp3")

        else:
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.subheader("Translated Text:")
            st.write(translated_text)
            st.markdown('</div>', unsafe_allow_html=True)