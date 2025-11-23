#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
from pathlib import Path

# Configuration de la page
st.set_page_config(
    page_title="Détermination des Visas d'Affaires",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personnalisé pour une belle interface
st.markdown("""
    <style>
    .main {
        background: #ffffff;
    }
    .stApp {
        background: #ffffff;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1 {
        color: #667eea;
        text-align: center;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        color: #666666;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .stSelectbox label {
        color: #333333 !important;
        font-weight: 600;
        font-size: 1.1rem;
    }
    .stButton > button {
        background: #283C78;
        color: white;
        font-size: 1.2rem;
        font-weight: 700;
        padding: 0.8rem 2rem;
        border: none;
        border-radius: 50px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 1rem;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
        background: #1a2a5a;
    }
    .result-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        margin-top: 2rem;
    }
    .visa-type {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        font-size: 1.3rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    .conditions-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        font-size: 1.05rem;
        line-height: 1.8;
    }
    .info-icon {
        font-size: 3rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    .form-container {
        background: #f8f9fa;
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        margin-top: 2rem;
    }
    .header-icon {
        text-align: center;
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    .divider {
        height: 2px;
        background: #e0e0e0;
        margin: 1.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Fonction pour charger les données
@st.cache_data
def load_visa_data():
    """Charge les données du fichier Excel"""
    try:
        # Chemin relatif vers le dossier pages (même dossier que le script)
        file_path = Path(__file__).parent / "Visas_Affaires_Court_Sejour_Mondial.xlsx"
        
        # Si le fichier n'existe pas, essayer d'autres emplacements
        if not file_path.exists():
            # Essayer dans le dossier ressources
            file_path = Path(__file__).parent.parent / "ressources" / "Visas_Affaires_Court_Sejour_Mondial.xlsx"
        
        if not file_path.exists():
            # Essayer dans le dossier parent
            file_path = Path(__file__).parent.parent / "Visas_Affaires_Court_Sejour_Mondial.xlsx"
        
        if not file_path.exists():
            st.error(f"❌ Fichier Excel introuvable.")
            st.info(f"📁 Placez le fichier 'Visas_Affaires_Court_Sejour_Mondial.xlsx' dans le dossier 'pages'")
            return None
        
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du fichier : {str(e)}")
        return None

# Fonction pour rechercher le visa
def find_visa_info(df, nationalite, pays_origine, pays_destination, duree, type_sejour):
    """Recherche les informations de visa correspondantes"""
    
    # Filtrer les données
    mask = (
        (df['Nationalité'].str.lower() == nationalite.lower()) &
        (df['Pays d\'origine'].str.lower() == pays_origine.lower()) &
        (df['Pays de destination'].str.lower() == pays_destination.lower()) &
        (df['Durée du séjour'].str.lower() == duree.lower()) &
        (df['Type de séjour'].str.lower() == type_sejour.lower())
    )
    
    result = df[mask]
    
    if not result.empty:
        return result.iloc[0]['Type de visa requis'], result.iloc[0]['Conditions d\'obtention du visa']
    else:
        # Recherche plus souple si aucun résultat exact
        mask_flexible = (
            (df['Nationalité'].str.lower() == nationalite.lower()) &
            (df['Pays de destination'].str.lower() == pays_destination.lower())
        )
        result_flexible = df[mask_flexible]
        
        if not result_flexible.empty:
            return result_flexible.iloc[0]['Type de visa requis'], result_flexible.iloc[0]['Conditions d\'obtention du visa']
        else:
            return None, None

# En-tête de l'application
st.markdown('<h1>Visas d\'Affaires</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Trouvez rapidement le visa requis pour les déplacements professionnels internationaux de vos collaborateurs</p>', unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Charger les données
df = load_visa_data()

if df is not None:
    # Créer trois colonnes pour le formulaire et les résultats
    col1, col2, col3 = st.columns([1, 1, 1.2])
    
    with col1:
        st.markdown("### 👤 Informations collaborateur")
        st.markdown("")
        
        # Menu déroulant pour la nationalité
        nationalites = ["-- Sélectionnez --"] + sorted(df['Nationalité'].unique().tolist())
        nationalite = st.selectbox(
            "🌐 Nationalité",
            options=nationalites,
            help="Sélectionnez la nationalité du collaborateur"
        )
        
        # Menu déroulant pour le pays d'origine
        pays_origines = ["-- Sélectionnez --"] + sorted(df['Pays d\'origine'].unique().tolist())
        pays_origine = st.selectbox(
            "🏠 Pays d'origine",
            options=pays_origines,
            help="Sélectionnez le pays de départ"
        )
        
        # Menu déroulant pour le type de séjour
        types_sejour = ["-- Sélectionnez --"] + sorted(df['Type de séjour'].unique().tolist())
        type_sejour = st.selectbox(
            "💼 Type de séjour",
            options=types_sejour,
            help="Sélectionnez le type de déplacement"
        )
    
    with col2:
        st.markdown("### 🎯 Destination et durée")
        st.markdown("")
        
        # Menu déroulant pour le pays de destination
        pays_destinations = ["-- Sélectionnez --"] + sorted(df['Pays de destination'].unique().tolist())
        pays_destination = st.selectbox(
            "📍 Pays de destination",
            options=pays_destinations,
            help="Sélectionnez le pays de destination"
        )
        
        # Menu déroulant pour la durée du séjour
        durees = ["-- Sélectionnez --"] + sorted(df['Durée du séjour'].unique().tolist())
        duree = st.selectbox(
            "⏱️ Durée du séjour",
            options=durees,
            help="Sélectionnez la durée prévue du séjour"
        )
        
        # Bouton de recherche
        st.markdown("")
        rechercher = st.button("🔍 Déterminer le Visa requis")
    
    # Colonne 3 pour les résultats
    with col3:
        st.markdown("### 📋 Résultat de la recherche")
        st.markdown("")
        
        # Affichage des résultats
        if rechercher:
            # Vérifier que tous les champs sont remplis
            if (nationalite == "-- Sélectionnez --" or 
                pays_origine == "-- Sélectionnez --" or 
                pays_destination == "-- Sélectionnez --" or 
                duree == "-- Sélectionnez --" or 
                type_sejour == "-- Sélectionnez --"):
                st.warning("⚠️ Veuillez remplir tous les champs du formulaire avant de lancer la recherche.")
            else:
                with st.spinner("🔄 Recherche en cours..."):
                    visa_type, conditions = find_visa_info(
                        df, nationalite, pays_origine, pays_destination, duree, type_sejour
                    )
                
                if visa_type and conditions:
                    # Afficher le récapitulatif compact
                    st.markdown(f"""
                    <div style="padding: 0.8rem; background: #f0f2f6; border-radius: 10px; margin-bottom: 0.8rem;">
                        <div style="font-weight: 600; color: #283C78; font-size: 0.9rem; margin-bottom: 0.3rem;">👤 Nationalité</div>
                        <div style="font-size: 0.95rem;">{nationalite}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div style="padding: 0.8rem; background: #f0f2f6; border-radius: 10px; margin-bottom: 0.8rem;">
                        <div style="font-weight: 600; color: #283C78; font-size: 0.9rem; margin-bottom: 0.3rem;">🏠 → 📍 Trajet</div>
                        <div style="font-size: 0.95rem;">{pays_origine} → {pays_destination}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div style="padding: 0.8rem; background: #f0f2f6; border-radius: 10px; margin-bottom: 1rem;">
                        <div style="font-weight: 600; color: #283C78; font-size: 0.9rem; margin-bottom: 0.3rem;">⏱️ Durée</div>
                        <div style="font-size: 0.95rem;">{duree}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("---")
                    
                    # Type de visa
                    st.markdown(f"""
                    <div style="background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 1rem; border-radius: 10px; text-align: center; font-weight: 700; margin-bottom: 1rem; font-size: 1.1rem;">
                        🛂 {visa_type}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Conditions d'obtention
                    st.markdown("**📄 Conditions d'obtention**")
                    st.markdown(f"""
                    <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; border-left: 5px solid #667eea; font-size: 0.9rem; line-height: 1.6;">
                        {conditions}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("")
                    st.info("💡 Informations à titre indicatif. Vérifiez auprès des autorités consulaires.", icon="ℹ️")
                    
                else:
                    st.warning("""
                    **⚠️ Aucune correspondance trouvée**
                    
                    Les critères sélectionnés ne correspondent à aucune entrée dans notre base de données.
                    
                    **Suggestions :**
                    - Vérifiez la combinaison nationalité/origine/destination
                    - Essayez avec des critères plus généraux
                    - Contactez notre service pour une assistance personnalisée
                    """)
        else:
            st.info("👈 Remplissez le formulaire et cliquez sur le bouton pour obtenir le résultat.", icon="ℹ️")

else:
    st.error("""
    ❌ **Impossible de charger les données**
    
    Le fichier Excel des visas n'a pas pu être chargé. 
    Veuillez vous assurer que le fichier 'Visas_Affaires_Court_Sejour_Mondial.xlsx' 
    est présent dans le répertoire approprié.
    """)