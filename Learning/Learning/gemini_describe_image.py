import streamlit as st
import google.generativeai as gen_ai
from PIL import Image
import io

# Configuration de l'API Google Generative AI
GEN_API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"  # Remplacez par votre clé API
gen_ai.configure(api_key=GEN_API_KEY)

# Titre de l'application
st.title("Analyse d'image avec Google Gemini")

# Charge une image de l'utilisateur
uploaded_image = st.file_uploader("Chargez une image (formats acceptés : PNG, JPEG, WEBP, HEIC, HEIF)", 
                                   type=["png", "jpeg", "jpg", "webp", "heic", "heif"])

# Champ de saisie pour la question (facultatif)
user_question = st.text_input("Posez une question sur l'image (facultatif)")

# Bouton pour analyser l'image
if st.button("Analyser l'image"):
    if uploaded_image:
        try:
            # Charger l'image en mémoire
            image = Image.open(uploaded_image)
            
            
            # Construire le prompt pour le modèle
            prompt = "Décrivez cette image."
            if user_question:
                prompt += f" {user_question}"
            
            # Envoyer la requête au modèle Gemini
            model = gen_ai.GenerativeModel(model_name="gemini-1.5-pro")
            response = model.generate_content([prompt, image])
            
            # Afficher la réponse
            st.image(image, caption="Image chargée", use_column_width=True)
            st.subheader("Réponse générée :")
            st.write(response.text)
        
        except Exception as e:
            st.error(f"Erreur lors du traitement de l'image : {str(e)}")
    else:
        st.warning("Veuillez charger une image avant d'analyser.")
