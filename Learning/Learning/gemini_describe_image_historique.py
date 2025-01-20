import streamlit as st
import google.generativeai as gen_ai
from PIL import Image
import io

# Configuration de l'API Google Generative AI
GEN_API_KEY = "AIzaSyBmgCgeR2Ak4qZf8NItR-5j_VRsrrng-QY"  # Remplacez par votre clé API
gen_ai.configure(api_key=GEN_API_KEY)

# Titre de l'application
st.title("Analyse d'image avec Google Gemini")

# Initialiser l'historique dans la session
if "history" not in st.session_state:
    st.session_state.history = []

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
            st.image(image, caption="Image chargée", use_container_width=True)
            st.subheader("Réponse générée :")
            st.write(response.text)
            
            # Enregistrer dans l'historique
            st.session_state.history.append({
                "image": uploaded_image.name,
                "question": user_question if user_question else "Aucune",
                "response": response.text
            })
        
        except Exception as e:
            st.error(f"Erreur lors du traitement de l'image : {str(e)}")
    else:
        st.warning("Veuillez charger une image avant d'analyser.")

# Afficher l'historique des actions
st.subheader("Historique des actions")
if st.session_state.history:
    for idx, entry in enumerate(st.session_state.history):
        st.write(f"### Action {idx + 1}")
        st.write(f"- **Image :** {entry['image']}")
        st.write(f"- **Question :** {entry['question']}")
        st.write(f"- **Réponse :** {entry['response']}")
else:
    st.info("Aucune action enregistrée pour le moment.")
