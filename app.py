import streamlit as st
from openai import OpenAI
import os

# Create OpenAI client using API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Load prompt template
with open("prompt_template.txt", "r") as f:
    template = f.read()

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
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful AI interview coach."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            answer = response.choices[0].message.content
            st.success("Answer generated!")
            st.text_area("AI Response:", value=answer, height=300)
            st.download_button("💾 Save Answer", data=answer, file_name="interview_answer.txt")
