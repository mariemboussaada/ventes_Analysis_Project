import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------------
# Configurer style
# ------------------------------
sns.set_style("whitegrid")
st.set_page_config(page_title="Dashboard Ventes", layout="wide")

# ------------------------------
# Charger le dataset
# ------------------------------
data = pd.read_csv("ventes_data.csv")  # adapte le chemin si besoin
data['produit'] = data['produit'].fillna('Inconnu')
data['categorie'] = data['categorie'].fillna('Inconnu')
data['quantité'] = data['quantité'].fillna(0)
data = data.dropna(subset=['date'])
data['date'] = pd.to_datetime(data['date'], errors='coerce')

# ------------------------------
# Titre
# ------------------------------
st.title("📊 Dashboard Ventes Analysis")
st.markdown("Analyse interactive des ventes pour prendre des décisions stratégiques.")

# ------------------------------
# Sidebar - Filtres
# ------------------------------
st.sidebar.header("📌 Filtres interactifs")
filtre_region = st.sidebar.multiselect(
    "Région", options=data['region'].unique(), default=data['region'].unique()
)
filtre_categorie = st.sidebar.multiselect(
    "Catégorie", options=data['categorie'].unique(), default=data['categorie'].unique()
)

# Slider pour l'année avec vérification
if data['date'].dt.year.nunique() > 1:
    filtre_annee = st.sidebar.slider(
        "Année",
        int(data['date'].dt.year.min()),
        int(data['date'].dt.year.max()),
        (int(data['date'].dt.year.min()), int(data['date'].dt.year.max()))
    )
else:
    annee_unique = int(data['date'].dt.year.min())
    filtre_annee = (annee_unique, annee_unique)
    st.sidebar.info(f"Seulement l'année {annee_unique} est disponible dans les données.")

# Appliquer les filtres
data_filtre = data[
    (data['region'].isin(filtre_region)) &
    (data['categorie'].isin(filtre_categorie)) &
    (data['date'].dt.year.between(filtre_annee[0], filtre_annee[1]))
]

# ------------------------------
# KPIs
# ------------------------------
st.subheader("📈 Indicateurs clés")
col1, col2, col3 = st.columns(3)
col1.metric("💰 Ventes totales", f"{data_filtre['prix_total'].sum():,.2f} €")
col2.metric("📦 Quantité totale", f"{data_filtre['quantité'].sum():,.0f}")
col3.metric("🪙 Prix moyen", f"{data_filtre['prix_total'].mean():,.2f} €")

# ------------------------------
# Graphiques principaux
# ------------------------------
st.markdown("---")
st.subheader("🎯 Top Analyses")

# Top Produits et Catégories côte à côte
top_prod = data_filtre.groupby('produit')['prix_total'].sum().sort_values(ascending=False).head(5)
ventes_cat = data_filtre.groupby('categorie')['prix_total'].sum().sort_values(ascending=False)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🏆 Top 5 Produits")
    fig, ax = plt.subplots()
    sns.barplot(x=top_prod.values, y=top_prod.index, palette="viridis", ax=ax)
    ax.set_xlabel("Ventes totales (€)")
    ax.set_ylabel("Produit")
    st.pyplot(fig)

with col2:
    st.markdown("### 📊 Ventes par Catégorie")
    fig2, ax2 = plt.subplots()
    sns.barplot(x=ventes_cat.values, y=ventes_cat.index, palette="coolwarm", ax=ax2)
    ax2.set_xlabel("Ventes totales (€)")
    ax2.set_ylabel("Catégorie")
    st.pyplot(fig2)

# Ventes par région
st.subheader("🌍 Ventes par Région")
ventes_region = data_filtre.groupby('region')['prix_total'].sum().sort_values(ascending=False)
fig3, ax3 = plt.subplots()
sns.barplot(x=ventes_region.values, y=ventes_region.index, palette="magma", ax=ax3)
ax3.set_xlabel("Ventes totales (€)")
ax3.set_ylabel("Région")
st.pyplot(fig3)

# Tendance des ventes
st.subheader("⏳ Tendance des ventes dans le temps")
ventes_temps = data_filtre.groupby('date')['prix_total'].sum()
fig4, ax4 = plt.subplots(figsize=(10,4))
ventes_temps.plot(ax=ax4, color="teal")
ax4.set_ylabel("Ventes totales (€)")
ax4.set_xlabel("Date")
st.pyplot(fig4)

# Heatmap
st.subheader("🔥 Heatmap des ventes par Région et Catégorie")
heatmap_data = data_filtre.pivot_table(
    index='region', columns='categorie', values='prix_total', aggfunc='sum', fill_value=0
)
fig5, ax5 = plt.subplots(figsize=(10,5))
sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="YlOrRd", ax=ax5)
st.pyplot(fig5)

# ------------------------------
# Conclusion et recommandations
# ------------------------------
st.markdown("---")
st.subheader("💡 Conclusions et recommandations")
st.markdown("""
- Les régions et catégories les plus performantes sont clairement identifiées.  
- Le top 5 des produits représente une part importante du chiffre d'affaires.  
- Suivre les ventes dans le temps permet de détecter les périodes creuses et de lancer des promotions ciblées.  
- Les données peuvent aider à **optimiser la stratégie commerciale**, la gestion des stocks et la planification marketing.
""")
