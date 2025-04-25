import streamlit as st
import requests

st.set_page_config(page_title="🧠 Your Own Interview Copilot")

st.title("🧠 Your Own Interview Copilot")
st.write("Type any interview question and get a smart answer based on your profile.")

question = st.text_input("Enter your interview question:")

if st.button("Generate Answer") and question:
    with st.spinner("Generating answer..."):

        headers = {
            "Authorization": f"Bearer {st.secrets['OPENROUTER_API_KEY']}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://your-app-name.streamlit.app",  # 🔁 replace with your actual app URL
            "X-Title": "Your Own Interview Copilot"
        }

        body = {
            "model": "mistral-7b-instruct",  # You can also try: "mixtral-8x7b", "openchat", etc.
            "messages": [
                {"role": "system", "content": "You are a helpful AI trained to answer technical interview questions like a senior network engineer."},
                {"role": "user", "content": question}
            ]
        }

        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=body
            )
            response.raise_for_status()
            output = response.json()
            st.success("Answer generated!")
            st.write(output['choices'][0]['message']['content'])

        except Exception as e:
            st.error("Something went wrong.")
            st.json({"error": str(e)})
