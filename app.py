import streamlit as st
import requests

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
    return response.json()

question = st.text_input("Enter your interview question:")
if st.button("Generate Answer") and question:
    with st.spinner("Generating answer..."):
        payload = {
            "model": "mistralai/mistral-7b-instruct:free",
            "messages": [{"role": "user", "content": question}],
        }
        output = query(payload)
        st.write(output['choices'][0]['message']['content'])
