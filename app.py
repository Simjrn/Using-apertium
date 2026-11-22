import requests
import streamlit as st

st.title("Apertium Translator")

# Language codes (use 3-letter ISO 639-3 codes like 'eng', 'spa', 'cat')
LANGS = {"English": "eng", "Spanish": "spa", "Catalan": "cat", "French": "fra"}

col1, col2 = st.columns(2)
src_lang = col1.selectbox("From", list(LANGS.keys()), index=0)
tgt_lang = col2.selectbox("To", list(LANGS.keys()), index=1)

text = st.text_area("Enter text to translate:", "Hello, world!")

if st.button("Translate"):
  if text.strip():
    url = "https://apertium.org"
    params = {"langpair": f"{LANGS[src_lang]}|{LANGS[tgt_lang]}", "q": text}
    try:
      response = requests.get(url, params=params, timeout=10)
      response.raise_for_status()
      data = response.json()

      if data.get("responseStatus") == 200:
        st.success(data["responseData"]["translatedText"])
      else:
        st.error(data.get("responseDetails", "Language pair not supported."))
    except requests.exceptions.RequestException as e:
      st.error(f"API request failed: {e}")
