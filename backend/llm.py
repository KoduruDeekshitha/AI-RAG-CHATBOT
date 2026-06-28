import requests
ollama_url="http://localhost:11434/api/generate"
def generate_answer(prompt):
    try:
        response=requests.post(
            ollama_url,json={
                "model":"llama3.2",
                "prompt":prompt,
                "stream":False 
        },timeout=60
    )
        response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.Timeout:
        return "The AI took too long to respond."
    except Exception as e:
        return f"Error:{e}"