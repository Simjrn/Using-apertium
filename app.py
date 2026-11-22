import requests
import streamlit as st

st.title("Apertium Translator")

LANGS = {"English": "eng", "Spanish": "spa", "Catalan": "cat", "French": "fra"}

col1, col2 = st.columns(2)
src_lang = col1.selectbox("From", list(LANGS.keys()), index=0)
tgt_lang = col2.selectbox("To", list(LANGS.keys()), index=1)

text = st.text_area("Enter text to translate:", "Hello, world!")

if st.button("Translate"):
  if text.strip():
    url = "https://apertium.org"
    params = {"langpair": f"{LANGS[src_lang]}|{LANGS[tgt_lang]}", "q": text}
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        ),
        "Accept": "application/json",
    }

    try:
      response = requests.get(url, params=params, headers=headers, timeout=15)

      # Check if the response is actually JSON before parsing
      if "application/json" not in response.headers.get("Content-Type", ""):
        st.error(f"Server returned non-JSON (Status {response.status_code}):")
        st.code(response.text[:500])  # Shows the HTML error or blank body
      else:
        data = response.json()
        if data.get("responseStatus") == 200:
          st.success(data["responseData"]["translatedText"])
        else:
          st.error(
              data.get("responseDetails", "Language pair not supported.")
          )

    except requests.exceptions.RequestException as e:
      st.error(f"Request failed: {e}")
