import streamlit as st
from transformers import pipeline

# Load the model (cached for fast responses)
@st.cache_resource
def load_model():
    return pipeline("text-generation", model="microsoft/DialoGPT-medium")

generator = load_model()

st.set_page_config(page_title="Your Own Interview Copilot", layout="centered")

st.title("🧠 Your Own Interview Copilot")
st.write("Type any interview question and get a smart answer based on your profile.")

question = st.text_area("Enter your interview question:")

if st.button("Generate Answer"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Generating answer..."):
            response = generator(question, max_length=150, num_return_sequences=1)
            answer = response[0]['generated_text']
            st.success("Answer generated!")
            st.text_area("AI Response:", value=answer, height=300)
            st.download_button("💾 Save Answer", data=answer, file_name="interview_answer.txt")
