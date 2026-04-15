import streamlit as st
import requests
import base64
from PIL import Image
import io

API_URL = "https://router.huggingface.co/hf-inference/models/Salesforce/blip-image-captioning-large"
HEADERS = {"Authorization": "Bearer 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"}  # your token

# ---- DEBUG LINE ----
st.write("Token starts with:", HEADERS["Authorization"][:20])

def image_to_text(image_bytes):
    try:
        encoded = base64.b64encode(image_bytes).decode("utf-8")
        payload = {"inputs": encoded}
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)
        st.write("Status code:", response.status_code)  # DEBUG
        st.write("Raw response:", response.text[:300])   # DEBUG
        
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
        if isinstance(result, list) and len(result) > 0:
            return result[0].get("generated_text", "No text generated.")
        elif isinstance(result, dict) and "error" in result:
            return f"❌ API Error: {result['error']}"
        else:
            return f"Unexpected response: {result}"

    except requests.exceptions.Timeout:
        return "❌ Request timed out. Please try again."
    except Exception as e:
        return f"❌ Error: {str(e)}"

st.title("🖼️ Image to Text Converter")
st.write("Upload an image and AI will describe what it sees!")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    img_bytes = io.BytesIO()
    image.save(img_bytes, format="PNG")
    img_bytes = img_bytes.getvalue()

    if st.button("Generate Text"):
        with st.spinner("Analyzing image..."):
            result = image_to_text(img_bytes)
        st.subheader("📝 Generated Description:")
        st.success(result)
