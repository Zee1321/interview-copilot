import streamlit as st
import openai

# Load API key securely from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Load the prompt template from file
with open("prompt_template.txt", "r") as f:
    template = f.read()

# Set Streamlit page configuration
st.set_page_config(page_title="Your Own Interview Copilot", layout="centered")

# UI layout
st.title("🧠 Your Own Interview Copilot")
st.write("Type any interview question and get a smart answer based on your profile.")

# Input box for user question
question = st.text_area("Enter your interview question:")

# When button is clicked
if st.button("Generate Answer"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        # Prepare the prompt
        prompt = template.replace("{question}", question)

        with st.spinner("Generating answer..."):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",  # use gpt-4 if your key supports it
                    messages=[
                        {"role": "system", "content": "You are a helpful AI interview coach."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=500
                )
                answer = response['choices'][0]['message']['content']
                st.success("Answer generated!")
                st.text_area("AI Response:", value=answer, height=300)
                st.download_button("💾 Save Answer", data=answer, file_name="interview_answer.txt")

            except Exception as e:
                st.error(f"An error occurred: {e}")
