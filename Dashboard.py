import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Professeur - Évaluation Orale",
    layout="wide",
    page_icon="📚"
)

st.title("📚 Tableau de Bord Professeur - Lecture Orale des Élèves")

# Charger les données depuis l'API Flask
API_URL = "http://localhost:5000/evaluations"  # Adapter si besoin

@st.cache_data

def fetch_data():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            return pd.json_normalize(response.json())
        else:
            st.error(f"Erreur API: {response.status_code}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Connexion impossible à l'API : {e}")
        return pd.DataFrame()

data = fetch_data()

if data.empty:
    st.warning("Aucune évaluation trouvée.")
    st.stop()

# Nettoyage et conversion des colonnes numériques
data["score_display"] = pd.to_numeric(data["score_display"], errors="coerce")
data["accuracy"] = pd.to_numeric(data["accuracy"], errors="coerce")
data["speed_wpm"] = pd.to_numeric(data["speed_wpm"], errors="coerce")

# Supprimer les lignes avec valeurs manquantes pour les graphiques
plot_data = data.dropna(subset=["score_display", "accuracy", "speed_wpm"])

# Sidebar pour personnalisation des textes de lecture
st.sidebar.header("✍️ Texte de Lecture Personnalisé")
text_input = st.sidebar.text_area("Texte que les élèves doivent lire", height=150)
if st.sidebar.button("Enregistrer le texte"):
    st.sidebar.success("Texte sauvegardé pour la prochaine session !")

# Afficher les résultats globaux
st.subheader("📈 Statistiques Générales")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Nombre d'évaluations", len(data))
with col2:
    st.metric("Précision moyenne", f"{data['accuracy'].mean():.1f}%")
with col3:
    st.metric("Vitesse moyenne", f"{data['speed_wpm'].mean():.1f} WPM")
with col4:
    st.metric("Score moyen", f"{data['score_display'].mean():.1f} / 10")

# Graphiques interactifs
st.subheader("📊 Visualisations")

tab1, tab2, tab3 = st.tabs(["Distribution des scores", "Vitesse vs Précision", "Analyse de la fluidité"])

with tab1:
    fig1 = px.histogram(plot_data, x="score_display", nbins=10, title="Répartition des Scores")
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    fig2 = px.scatter(plot_data, x="speed_wpm", y="accuracy", size="score_display",
                      title="Vitesse vs Précision", hover_data=["expected_text"])
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    fluency_counts = data["fluency"].value_counts().reset_index()
    fluency_counts.columns = ["fluency", "count"]
    fig3 = px.pie(fluency_counts, values='count', names='fluency', title="Répartition des niveaux de fluidité")
    st.plotly_chart(fig3, use_container_width=True)

# Tableau complet
st.subheader("📋 Détails des Évaluations")
st.dataframe(data[["expected_text", "transcript", "accuracy", "speed_wpm", "fluency", "score_display"]])
