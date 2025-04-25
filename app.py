import streamlit as st
from transformers import pipeline, set_seed

# Load generator once (cache for performance)
@st.cache_resource
def load_generator():
    generator = pipeline('text-generation', model='gpt2')
    set_seed(42)
    return generator

generator = load_generator()

st.set_page_config(page_title="Your Own Interview Copilot", layout="centered")

st.title("🧠 Your Own Interview Copilot")
st.write("Type any interview question and get a smart answer based on your profile.")

question = st.text_area("Enter your interview question:")

if st.button("Generate Answer"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Generating answer..."):
            result = generator(question, max_length=100, num_return_sequences=1)
            answer = result[0]['generated_text']
            st.success("Answer generated!")
            st.text_area("AI Response:", value=answer, height=250)
            st.download_button("💾 Save Answer", data=answer, file_name="interview_answer.txt")
