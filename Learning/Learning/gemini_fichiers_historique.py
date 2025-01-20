import google.generativeai as gen_ai
import streamlit as st
import mimetypes

# Configuration de l'API
GEN_API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"  # Remplacez par votre clé API
gen_ai.configure(api_key=GEN_API_KEY)

# Fonction pour générer du contenu à partir d'un PDF
def generate_pdf_content(pdf_file, question):
    # Lire le contenu du fichier PDF
    pdf_bytes = pdf_file.read()

    # Détecter le type MIME du fichier
    mime_type, _ = mimetypes.guess_type(pdf_file.name)
    if mime_type is None:
        mime_type = "application/pdf"  # Spécifiez un type MIME par défaut

    try:
        # Utilisation de l'API pour télécharger le fichier avec le type MIME spécifié
        sample_pdf = gen_ai.upload_file(pdf_file, mime_type=mime_type)

        # Utilisation de l'API Gemini pour générer du contenu à partir du PDF
        model = gen_ai.GenerativeModel(model_name="gemini-1.5-flash")

        # Demande à l'API de générer une réponse
        response = model.generate_content([question, sample_pdf])
        return response.text
    except Exception as e:
        return f"Une erreur s'est produite : {e}"

# Fonction principale
def main():
    st.set_page_config(layout="wide")
    st.title("Chatbot PDF avec Gemini API")

    st.sidebar.title("Data Loader")
    st.sidebar.image("rag.png", width=500)

    # Permet à l'utilisateur de télécharger plusieurs fichiers PDF
    pdf_files = st.file_uploader("Téléchargez vos fichiers PDF", type="pdf", accept_multiple_files=True)

    if pdf_files:
        st.write(f"{len(pdf_files)} fichiers PDF téléchargés avec succès.")
        
        # Créer une session pour garder l'état des questions et réponses
        if 'conversation' not in st.session_state:
            st.session_state.conversation = []  # Liste vide pour stocker les échanges

        # Choisir le fichier sur lequel poser une question
        selected_file = st.selectbox("Sélectionnez un fichier PDF", [f.name for f in pdf_files])
        selected_pdf_file = next(f for f in pdf_files if f.name == selected_file)

        # Champ de saisie pour la question
        user_question = st.text_input("Posez votre question :")
        
        if user_question:
            with st.spinner("Chargement..."):
                # Ajouter la question à la conversation
                st.session_state.conversation.append({"role": "user", "content": user_question})
                
                # Générer la réponse à partir du PDF sélectionné et de la question
                response_text = generate_pdf_content(selected_pdf_file, user_question)
                
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
