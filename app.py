import streamlit as st
import openai
import os

# Set up the OpenAI client using the new SDK format
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Load prompt template
with open("prompt_template.txt", "r") as f:
    template = f.read()

# Streamlit page settings
st.set_page_config(page_title="Your Own Interview Copilot", layout="centered")

st.title("🧠 Your Own Interview Copilot")
st.write("Type any interview question and get a smart answer based on your profile.")

# User input
question = st.text_area("Enter your interview question:")

# Generate button
if st.button("Generate Answer"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        prompt = template.replace("{question}", question)
        with st.spinner("Generating answer..."):
            try:
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
            except Exception as e:
                st.error(f"An error occurred: {e}")
