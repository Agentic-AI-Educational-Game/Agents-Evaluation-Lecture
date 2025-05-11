# 📚 Évaluation de la Lecture

Une API Flask pour évaluer la qualité de la lecture orale chez les enfants, avec transcription, évaluation de la vitesse, de la prononciation et de la fluidité.

---

## 🚀 Instructions

### 🔨 1. Construction de l'image Docker

```bash
docker build -t readeval-app .
```

### ▶️ 2. Exécution du conteneur

```bash
docker run -p 5000:5000 readeval-app
```

---

## 📥 Endpoint API

### POST `/evaluate`

#### Body (form-data) :
- `audio`: fichier audio (format `.mp3`, `.wav`, etc.)
- `expected_text`: texte que l’enfant était censé lire

#### Réponse :
```json
{
  "accuracy": "98%",
  "speed": "120 WPM",
  "fluency": "good",
  "pron_feedback": "Très bien joué ! Essaie de mieux articuler quelques mots.",
  "score": "4.5 / 5 stars",
  "transcript": "Texte transcrit à partir de l’audio"
}
```
![image](https://github.com/user-attachments/assets/370737c2-b752-4b0d-a8fa-b5593190868e)

---

## 🧠 Modèles utilisés

- **Whisper (OpenAI)** : pour la transcription vocale.
- **Groq (LLaMA)** : pour générer un retour pédagogique personnalisé.

---

## 📁 Uploads

Les fichiers audios envoyés sont sauvegardés dans le dossier `uploads/`.

---

## ⚠️ Remarques

- Cette API est conçue pour fonctionner **en local**.
- Utiliser uniquement à des fins de test/développement.
- Prévoir une connexion internet pour le modèle Whisper et Groq.

---

## 👨‍💻 Auteur

Projet éducatif développé avec ❤️ par l'équipe Agentic AI Game.
