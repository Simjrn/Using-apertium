import requests
import streamlit as st

st.title("Apertium Translator")

LANGS = {"English": "eng", "Spanish": "spa", "Catalan": "cat", "French": "fra", "Arpitan": "frp"}

col1, col2 = st.columns(2)
src_lang = col1.selectbox("From", list(LANGS.keys()), index=0)
tgt_lang = col2.selectbox("To", list(LANGS.keys()), index=1)

text = st.text_area("Enter text to translate:", "Hello, world!")

if st.button("Translate"):
  if text.strip():
    # Use beta.apertium.org and POST form data so it hits the APy backend directly
    url = "https://beta.apertium.org/apy/translate"
    payload = {
        "langpair": f"{LANGS[src_lang]}|{LANGS[tgt_lang]}",
        "q": text,
        "markUnknown": "no",
    }

    try:
      response = requests.post(url, data=payload, timeout=15)
      response.raise_for_status()
      data = response.json()

      if data.get("responseStatus") == 200:
        st.success(data["responseData"]["translatedText"])
      else:
        st.error(data.get("responseDetails", "Language pair not supported."))

    except Exception as e:
      st.error(f"Request failed: {e}")
