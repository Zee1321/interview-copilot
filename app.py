import streamlit as st
import requests

st.set_page_config(page_title="Your Own Interview Copilot")

st.title("🤯 Your Own Interview Copilot")
st.write("Type any interview question and get a smart answer based on your profile.")

question = st.text_area("Enter your interview question:", height=100)

if st.button("Generate Answer") and question:
    with st.spinner("Generating answer..."):

        try:
            headers = {
                "Authorization": f"Bearer {st.secrets['OPENROUTER_API_KEY']}",
                "Content-Type": "application/json"
            }

            data = {
                "model": "mistralai/mistral-7b-instruct",  # fast, free-tier compatible model on OpenRouter
                "messages": [
                    {"role": "system", "content": "You are a helpful interview assistant that answers concisely."},
                    {"role": "user", "content": question}
                ]
            }

            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=15
            )

            result = response.json()
            if "choices" in result:
                answer = result["choices"][0]["message"]["content"]
                st.success("Answer generated!")
                st.write("### AI Response:")
                st.write(answer)
            else:
                st.error("No answer returned. Please check API or try again later.")
                st.json(result)

        except Exception as e:
            st.error("Something went wrong.")
            st.exception(e)
