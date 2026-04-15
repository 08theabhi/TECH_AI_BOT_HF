import streamlit as st
import requests

API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn"
HEADERS = {"Authorization": "Bearer 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"}  # your real token

def summarize(text, max_length, min_length):
    payload = {
        "inputs": text,
        "parameters": {
            "max_length": max_length,
            "min_length": min_length,
            "do_sample": False
        }
    }
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)
        if response.status_code == 401:
            return "❌ Invalid HuggingFace token. Please check your token."
        elif response.status_code == 503:
            return "⏳ Model is loading, please wait 20 seconds and try again."
        elif response.status_code == 429:
            return "⚠️ Too many requests. Please wait a moment and try again."
        elif response.status_code == 404:
            return "❌ Model not found. Check the API URL."
        elif response.status_code != 200:
            return f"❌ API Error: Status code {response.status_code}"
        result = response.json()
        if isinstance(result, list) and len(result) > 0 and 'summary_text' in result[0]:
            return result[0]['summary_text']
        elif isinstance(result, dict) and 'error' in result:
            return f"❌ API Error: {result['error']}"
        else:
            return f"Unexpected response: {result}"
    except requests.exceptions.Timeout:
        return "❌ Request timed out. Please try again."
    except Exception as e:
        return f"❌ Error: {str(e)}"

st.title("🤖 AI Text Summarizer")
st.write("Enter a long text below, and get a concise summary!")

long_text = st.text_area("Enter text to summarize:", height=200)
max_length = st.slider("Max Summary Length", min_value=50, max_value=300, value=130)
min_length = st.slider("Min Summary Length", min_value=10, max_value=50, value=30)

if st.button("Summarize"):
    if long_text.strip():
        with st.spinner("Generating summary..."):
            result = summarize(long_text, max_length, min_length)
        st.subheader("Summary:")
        st.write(result)
    else:
        st.warning("⚠️ Please enter some text to summarize.")
