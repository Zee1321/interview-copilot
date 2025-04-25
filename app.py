import streamlit as st
import requests

# Load Hugging Face token from secrets
HF_TOKEN = st.secrets["HF_TOKEN"]

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

# Load the prompt template
with open("prompt_template.txt", "r") as f:
    template = f.read()

def query(payload):
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()

st.set_page_config(page_title="Your Own Interview Copilot", layout="centered")
st.title("🧠 Your Own Interview Copilot")
st.write("Type any interview question and get a smart answer based on your profile.")

question = st.text_area("Enter your interview question:")

if st.button("Generate Answer"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        prompt = template.replace("{question}", question)
        with st.spinner("Generating answer..."):
            try:
                output = query({"inputs": prompt})
                answer = output[0]["generated_text"].split("Answer:")[-1].strip()
                st.success("Answer generated!")
                st.text_area("AI Response:", value=answer, height=300)
                st.download_button("💾 Save Answer", data=answer, file_name="interview_answer.txt")
            except Exception as e:
                st.error(f"Something went wrong: {e}")
