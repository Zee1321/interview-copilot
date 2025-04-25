import streamlit as st
import requests

# Hugging Face API details
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
headers = {"Authorization": f"Bearer {st.secrets['HF_TOKEN']}"}

# Streamlit layout
st.set_page_config(page_title="Your Own Interview Copilot", layout="centered")
st.title("🧠 Your Own Interview Copilot")
st.write("Type any interview question and get a smart answer based on your profile.")

question = st.text_area("Enter your interview question:")

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

if st.button("Generate Answer"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Generating answer..."):
            output = query({"inputs": question})
            try:
                result = output[0]["generated_text"]
                st.success("Answer generated!")
                st.text_area("AI Response:", value=result, height=300)
                st.download_button("💾 Save Answer", data=result, file_name="interview_answer.txt")
            except Exception as e:
                st.error(f"Error generating answer: {output}")
