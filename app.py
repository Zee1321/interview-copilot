import streamlit as st
import requests

st.set_page_config(page_title="Your Own Interview Copilot")

st.title("🧠 Your Own Interview Copilot")
st.write("Type any interview question and get a smart answer based on your profile.")

question = st.text_input("Enter your interview question:")

def query(payload):
    headers = {
        "Authorization": f"Bearer {st.secrets['OPENROUTER_API_KEY']}",
        "Content-Type": "application/json"
    }
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload
    )
    try:
        return response.json()
    except Exception as e:
        return {"error": str(e), "raw_response": response.text}

if st.button("Generate Answer") and question.strip():
    with st.spinner("Generating answer..."):
        payload = {
            "model": "mistralai/mistral-7b-instruct",
            "messages": [
                {"role": "system", "content": "You are a helpful technical interview coach."},
                {"role": "user", "content": question}
            ]
        }
        output = query(payload)

        if "choices" in output and len(output["choices"]) > 0:
            st.success("Answer generated!")
            st.markdown("**AI Response:**")
            st.write(output["choices"][0]["message"]["content"])
        else:
            st.error("Something went wrong. See full output below.")
            st.json(output)
