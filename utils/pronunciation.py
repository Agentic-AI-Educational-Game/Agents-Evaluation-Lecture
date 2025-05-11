from openai import OpenAI

client = OpenAI(
    api_key="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",
    base_url="https://api.groq.com/openai/v1"
)

def get_pronunciation_feedback(user_text, expected_text):
    prompt = f"""
        Tu es un assistant éducatif dans un jeu pour enfants. 
        Tu dois évaluer la prononciation d’un enfant de manière douce, motivante et en français.
        Voici ce qu’il devait dire : « {expected_text} »
        Voici ce qu’on a entendu : « {user_text} »
        
        Donne un retour en **une seule phrase**, simple et encourageante, en français, comme si tu parlais à un enfant.
        """
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()
