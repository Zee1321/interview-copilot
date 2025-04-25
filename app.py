import streamlit as st
import requests

# Page setup
st.set_page_config(page_title="Your Own Interview Copilot", layout="centered")

st.title("🧠 Your Own Interview Copilot")
st.write("Type any technical interview question and get a smart, real-world answer powered by the Mistral AI model.")

# Input box
question = st.text_area("Enter your interview question:")

# OpenRouter API query function
def query(payload):
    headers = {
        "Authorization": f"Bearer {st.secrets['OPENROUTER_API_KEY']}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# Generate Answer button
if st.button("Generate Answer") and question.strip():
    with st.spinner("Generating answer..."):
        payload = {
            "model": "mistralai/mistral-7b-instruct",
            "messages": [
                {"role": "system", "content": "You are a helpful senior network engineer who answers technical interview questions in a clear and concise manner."},
                {"role": "user", "content": question}
            ]
        }
        output = query(payload)

        # Safely extract and display the response
        if "choices" in output and len(output["choices"]) > 0:
            answer = output["choices"][0]["message"]["content"]
            st.success("Answer generated!")
            st.text_area("AI Response:", value=answer, height=300)
            st.download_button("💾 Save Answer", data=answer, file_name="interview_answer.txt")
        else:
            st.error("Something went wrong.")
            st.json(output)
