
# donne un fichier à gemini et on garde l'historique des conversation.

import streamlit as st
import google.generativeai as gen_ai
import io

# Configuration de l'API
GEN_API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"  # Remplacez par votre clé API
gen_ai.configure(api_key=GEN_API_KEY)

# Fonction pour télécharger le fichier PDF et générer la réponse
def generate_pdf_content(pdf_file, question):
    # Convertir le fichier téléchargé en un format compatible avec l'API Gemini
    pdf_bytes = pdf_file.read()  # Lire le fichier binaire

    # Téléchargement du fichier PDF avec le type MIME spécifié
    sample_pdf = gen_ai.upload_file(
        io.BytesIO(pdf_bytes),  # Utiliser BytesIO pour lire les octets du fichier
        mime_type="application/pdf"  # Spécifier le type MIME
    )

    # Génération de contenu à partir du fichier PDF en posant une question
    model = gen_ai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content([question, sample_pdf])
    
    return response.text

def main():
    st.set_page_config(layout="wide")
    st.title("Chatbot PDF avec Gemini API")

    st.sidebar.title("Data Loader")
    st.sidebar.image("rag.png", width=500)

    # Permet à l'utilisateur de télécharger un fichier PDF
    pdf_file = st.file_uploader("Téléchargez votre fichier PDF", type="pdf")
    
    if pdf_file:
        st.write(f"Fichier {pdf_file.name} téléchargé avec succès.")
        
        # Créer une session pour garder l'état des questions et réponses
        if 'conversation' not in st.session_state:
            st.session_state.conversation = []  # Liste vide pour stocker les échanges

        # Champ de saisie pour la question
        user_question = st.text_input("Posez votre question :")
        
        if user_question:
            with st.spinner("Chargement..."):
                # Ajouter la question à la conversation
                st.session_state.conversation.append({"role": "user", "content": user_question})
                
                # Générer la réponse à partir du PDF et de la question
                response_text = generate_pdf_content(pdf_file, user_question)
                
                # Ajouter la réponse à la conversation
                st.session_state.conversation.append({"role": "bot", "content": response_text})
                
                # Afficher la réponse
                st.subheader("Réponse :")
                st.write(response_text)
        
        # Affichage de l'historique des questions et réponses
        if st.session_state.conversation:
            st.subheader("Historique de la conversation :")
            for exchange in st.session_state.conversation:
                role = exchange["role"]
                content = exchange["content"]
                if role == "user":
                    st.markdown(f"**Vous** : {content}")
                else:
                    st.markdown(f"**Bot** : {content}")
    
if __name__ == "__main__":
    main()
