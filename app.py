import requests

API_URL = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {st.secrets['OPENROUTER_API_KEY']}",
    "HTTP-Referer": "https://your-domain.com",  # replace with your deployed domain or localhost
    "Content-Type": "application/json"
}

def query_openrouter(question):
    body = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [
            {"role": "system", "content": "You are a helpful AI interview coach."},
            {"role": "user", "content": question}
        ]
    }
    response = requests.post(API_URL, headers=headers, json=body)
    return response.json()["choices"][0]["message"]["content"]
