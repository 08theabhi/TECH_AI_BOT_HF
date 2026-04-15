import streamlit as st
from groq import Groq

client = Groq(api_key="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")

def summarize(text, max_length, min_length):
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a text summarizer. Summarize the given text in minimum {min_length} words and maximum {max_length} words. Give only the summary, nothing else."
                },
                {
                    "role": "user",
                    "content": f"Summarize this text:\n\n{text}"
                }
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {str(e)}"

st.title("🤖 AI Text Summarizer")
st.write("Enter a long text below, and get a concise summary!")

long_text = st.text_area("Enter text to summarize:", height=200)
max_length = st.slider("Max Summary Length (words)", min_value=50, max_value=300, value=130)
min_length = st.slider("Min Summary Length (words)", min_value=10, max_value=50, value=30)

if st.button("Summarize"):
    if long_text.strip():
        with st.spinner("Generating summary..."):
            result = summarize(long_text, max_length, min_length)
        st.subheader("📝 Summary:")
        st.success(result)
    else:
        st.warning("⚠️ Please enter some text to summarize.")
