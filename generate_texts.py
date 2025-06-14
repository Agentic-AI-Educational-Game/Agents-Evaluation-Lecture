import httpx
import os
from flask import Flask, jsonify

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")

def generate_simple_text():
    prompt = """
    Tu es un assistant éducatif dans un jeu de lecture pour enfants de 6 à 9 ans.

    Génère un **texte de lecture très simple et court** pour un élève débutant :
    - Entre **6 et 9 phrases** simples et courtes
    - Utilise un vocabulaire **facile, mais légèrement plus riche**
    - Le texte doit être **éducatif** : il peut apprendre à l’enfant un fait, une règle ou une action utile (ex : l’hygiène, les animaux, la nature, les émotions…)
    - Raconte une petite **scène de la vie réelle ou scolaire**
    - Reste clair, positif et adapté aux enfants entre 6 et 9 ans

    Format attendu :
    Texte: ...
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

    content = response.json()["choices"][0]["message"]["content"]

    # Nettoyage simple du texte
    text = content.replace("Texte:", "").replace("\n", " ").strip()

    return {"text": text}

@app.route("/generate_llm_text", methods=["GET"])
def generate_text():
    try:
        result = generate_simple_text()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5002)
