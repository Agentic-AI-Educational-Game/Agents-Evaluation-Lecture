import httpx
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")

def get_pronunciation_feedback(user_text, expected_text):
    prompt = f"""
    Tu es un assistant éducatif dans un jeu pour enfants.
    Tu dois évaluer la prononciation d’un enfant de manière douce, motivante et en français.
    Voici ce qu’il devait dire : « {expected_text} »
    Voici ce qu’on a entendu : « {user_text} »

    Donne un retour en **une seule phrase**, simple et encourageante, en français, comme si tu parlais à un enfant.
    """

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    data = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = httpx.post("https://api.groq.com/openai/v1/chat/completions", json=data, headers=headers)
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"].strip()
