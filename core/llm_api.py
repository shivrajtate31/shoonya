import requests

def query_ollama_api(prompt, model="phi3"):
    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": model,
            "prompt": prompt,
            "stream": False
        })
        if response.ok:
            return response.json()["response"].strip()
        else:
            print(" API error:", response.text)
            return ""
    except Exception as e:
        print(f" Request error: {e}")
        return ""
