import httpx
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")

def get_pronunciation_feedback(user_text, expected_text):
    prompt = f"""
    Tu es un assistant éducatif bienveillant dans un jeu de lecture pour enfants.

    Ta mission est d’évaluer la prononciation d’un enfant de manière **encourageante, claire et adaptée à son âge (6 à 9 ans)**.

    Voici la phrase que l’enfant devait prononcer : « {expected_text} »
    Voici ce que l’on a entendu : « {user_text} »

    Donne un **feedback en français, sous forme d’un message direct à l’enfant**, en respectant les consignes suivantes :
    - Le retour doit être **positif et motivant**, même s’il y a des erreurs
    - Utilise un **langage simple, joyeux et adapté aux enfants**
    - Le **message ne doit pas dépasser deux phrases maximum**
    - Tu peux féliciter ou encourager à réessayer doucement
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
