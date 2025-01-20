import streamlit as st
import google.generativeai as gen_ai
from PIL import Image
import io

# Configuration de l'API Google Generative AI
GEN_API_KEY = "AIzaSyBmgCgeR2Ak4qZf8NItR-5j_VRsrrng-QY"  # Remplacez par votre clé API
gen_ai.configure(api_key=GEN_API_KEY)


# Fonction pour traiter les PDF
def generate_pdf_content(pdf_file, question):
    # Convertir le fichier PDF en format compatible
    pdf_bytes = pdf_file.read()
    sample_pdf = gen_ai.upload_file(
        io.BytesIO(pdf_bytes),
        mime_type="application/pdf"
    )
    # Générer une réponse
    model = gen_ai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content([question, sample_pdf])
    return response.text


# Fonction pour traiter les images
def generate_image_content(image, question):
    prompt = f"Décrivez cette image. {question}" if question else "Décrivez cette image."
    model = gen_ai.GenerativeModel(model_name="gemini-1.5-pro")
    response = model.generate_content([prompt, image])
    return response.text


# Fonction pour un chatbot simple
def generate_chat_response(question):
    model = gen_ai.GenerativeModel(model_name="gemini-1.5-pro")
    response = model.generate_content([question])
    return response.text


# Application principale
def main():
    st.set_page_config(layout="wide")
    st.title("Application Globale : Analyse d'Images, PDF et Chatbot avec Google Gemini")
    
    # Initialiser l'historique dans la session
    if "history" not in st.session_state:
        st.session_state.history = []

    # Barre latérale pour le mode
    mode = st.sidebar.selectbox(
        "Choisissez une fonctionnalité :",
        ["Analyse d'image", "Analyse de PDF", "Chatbot"]
    )

    # Section : Analyse d'image
    if mode == "Analyse d'image":
        st.header("Analyse d'image")
        uploaded_image = st.file_uploader("Chargez une image (formats acceptés : PNG, JPEG, WEBP, HEIC, HEIF)", 
                                          type=["png", "jpeg", "jpg", "webp", "heic", "heif"])
        user_question = st.text_input("Posez une question sur l'image (facultatif)")

        if st.button("Analyser l'image"):
            if uploaded_image:
                try:
                    image = Image.open(uploaded_image)
                    response_text = generate_image_content(image, user_question)
                    
                    st.image(image, caption="Image chargée", use_column_width=True)
                    st.subheader("Réponse générée :")
                    st.write(response_text)

                    st.session_state.history.append({
                        "type": "image",
                        "file": uploaded_image.name,
                        "question": user_question if user_question else "Aucune",
                        "response": response_text
                    })
                except Exception as e:
                    st.error(f"Erreur lors du traitement de l'image : {str(e)}")
            else:
                st.warning("Veuillez charger une image avant d'analyser.")

    # Section : Analyse de PDF
    elif mode == "Analyse de PDF":
        st.header("Analyse de PDF")
        pdf_file = st.file_uploader("Téléchargez votre fichier PDF", type="pdf")
        user_question = st.text_input("Posez une question sur le PDF :")

        if st.button("Analyser le PDF"):
            if pdf_file and user_question:
                try:
                    response_text = generate_pdf_content(pdf_file, user_question)
                    
                    st.subheader("Réponse générée :")
                    st.write(response_text)

                    st.session_state.history.append({
                        "type": "pdf",
                        "file": pdf_file.name,
                        "question": user_question,
                        "response": response_text
                    })
                except Exception as e:
                    st.error(f"Erreur lors du traitement du PDF : {str(e)}")
            else:
                st.warning("Veuillez charger un fichier PDF et poser une question.")

    # Section : Chatbot simple
    elif mode == "Chatbot":
        st.header("Chatbot")
        user_question = st.text_input("Posez une question au chatbot :")
        
        if st.button("Envoyer"):
            if user_question:
                try:
                    response_text = generate_chat_response(user_question)
                    
                    st.subheader("Réponse générée :")
                    st.write(response_text)

                    st.session_state.history.append({
                        "type": "chat",
                        "question": user_question,
                        "response": response_text
                    })
                except Exception as e:
                    st.error(f"Erreur lors de la génération de réponse : {str(e)}")
            else:
                st.warning("Veuillez poser une question au chatbot.")

    # Historique des interactions
    st.sidebar.subheader("Historique des interactions")
    if st.session_state.history:
        for idx, entry in enumerate(st.session_state.history):
            st.sidebar.write(f"### Interaction {idx + 1}")
            if entry["type"] == "image":
                st.sidebar.write(f"- **Type :** Analyse d'image")
                st.sidebar.write(f"- **Fichier :** {entry['file']}")
            elif entry["type"] == "pdf":
                st.sidebar.write(f"- **Type :** Analyse de PDF")
                st.sidebar.write(f"- **Fichier :** {entry['file']}")
            else:
                st.sidebar.write(f"- **Type :** Chatbot")
            st.sidebar.write(f"- **Question :** {entry['question']}")
            st.sidebar.write(f"- **Réponse :** {entry['response']}")
    else:
        st.sidebar.info("Aucune interaction enregistrée.")

# Exécuter l'application
if __name__ == "__main__":
    main()
