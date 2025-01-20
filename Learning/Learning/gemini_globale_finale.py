import streamlit as st
import google.generativeai as gen_ai
from PIL import Image
import io
import os
from datetime import datetime

# Configuration de l'API Google Generative AI
GEN_API_KEY = "AIzaSyBmgCgeR2Ak4qZf8NItR-5j_VRsrrng-QY"  # Remplacez par votre clé API
gen_ai.configure(api_key=GEN_API_KEY)

# Répertoires pour stocker les fichiers
IMAGE_DIR = "upload/images"
PDF_DIR = "upload/pdfs"
os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)

# Générer un nom de fichier unique basé sur l'horodatage
def generate_filename(original_name, directory):
    """
    Génère un nom de fichier unique basé sur l'horodatage actuel.

    :param original_name: Nom original du fichier (pour conserver l'extension).
    :param directory: Répertoire où le fichier sera stocké.
    :return: Chemin complet avec un nom de fichier unique.
    """
    # Générer un horodatage dans le format souhaité (YYYYMMDDHHMMSS)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    
    # Extraire l'extension du fichier
    extension = os.path.splitext(original_name)[1]
    
    # Retourner le chemin complet avec le répertoire, horodatage et extension
    return os.path.join(directory, f"{timestamp}{extension}")


# Fonction pour traiter les PDF
def generate_pdf_content(pdf_file, question):
    pdf_bytes = pdf_file.read()
    sample_pdf = gen_ai.upload_file(
        io.BytesIO(pdf_bytes),
        mime_type="application/pdf"
    )
    model = gen_ai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content([question, sample_pdf])
    return response.text

# Fonction pour traiter les images
def generate_image_content(image, question):
    model = gen_ai.GenerativeModel(model_name="gemini-1.5-pro")
    response = model.generate_content([question, image])
    return response.text

# Fonction pour un chatbot simple
def generate_chat_response(question):
    model = gen_ai.GenerativeModel(model_name="gemini-1.5-pro")
    response = model.generate_content([question])
    return response.text

# Application principale
def main():
    st.set_page_config(layout="wide")
    st.title("Application d'Analyse Générative : Chatbot, Images, et PDF avec Google Gemini")
    
    # Initialiser l'historique dans la session
    if "history" not in st.session_state:
        st.session_state.history = []

    # affichage d'un logo dans la barre latérale    
    st.sidebar.image("logo.png", use_container_width=True)

    # Barre latérale pour le mode
    mode = st.sidebar.selectbox(
        "Choisissez une fonctionnalité :",
        ["Chatbot", "Analyse d'image", "Analyse de PDF"]
    )

    # Section : Analyse d'image
    if mode == "Analyse d'image":
        st.header("Analyse d'image")
        uploaded_image = st.file_uploader("Chargez une image (formats acceptés : PNG, JPEG, WEBP, HEIC, HEIF)", 
                                          type=["png", "jpeg", "jpg", "webp", "heic", "heif"])
        user_question = st.text_input("Posez une question sur l'image")

        if st.button("Analyser l'image"):
            if uploaded_image and user_question:
                try:
                    # Sauvegarder l'image dans le répertoire upload/images
                    #image_path = os.path.join(IMAGE_DIR, uploaded_image.name)
                    image_path = generate_filename(uploaded_image.name, IMAGE_DIR)

                    with open(image_path, "wb") as f:
                        f.write(uploaded_image.read())

                    # Charger l'image pour traitement
                    image = Image.open(image_path)
                    response_text = generate_image_content(image, user_question)

                    st.image(image, caption="Image chargée", use_container_width=True)
                    st.subheader("Réponse générée :")
                    st.write(response_text)

                    # Enregistrer l'interaction dans l'historique
                    st.session_state.history.insert(0, {
                        "type": "image",
                        "file": image_path,
                        "question": user_question,
                        "response": response_text,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                except Exception as e:
                    st.error(f"Erreur lors du traitement de l'image : {str(e)}")
            else:
                st.warning("Veuillez charger une image avant d'analyser et poser une question.")

    # Section : Analyse de PDF
    elif mode == "Analyse de PDF":
        st.header("Analyse de PDF")
        pdf_file = st.file_uploader("Téléchargez votre fichier PDF", type="pdf")
        user_question = st.text_input("Posez une question sur le PDF :")

        if st.button("Analyser le PDF"):
            if pdf_file and user_question:
                try:
                    # Sauvegarder le PDF dans le répertoire upload/pdfs
                    #pdf_path = os.path.join(PDF_DIR, pdf_file.name)
                    pdf_path = generate_filename(pdf_file.name, PDF_DIR)

                    with open(pdf_path, "wb") as f:
                        f.write(pdf_file.read())

                    response_text = generate_pdf_content(open(pdf_path, "rb"), user_question)

                    st.subheader("Réponse générée :")
                    st.write(response_text)

                    # Enregistrer l'interaction dans l'historique
                    st.session_state.history.insert(0, {
                        "type": "pdf",
                        "file": pdf_path,
                        "question": user_question,
                        "response": response_text,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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

                    # Enregistrer l'interaction dans l'historique
                    st.session_state.history.insert(0, {
                        "type": "chat",
                        "question": user_question,
                        "response": response_text,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                except Exception as e:
                    st.error(f"Erreur lors de la génération de réponse : {str(e)}")
            else:
                st.warning("Veuillez poser une question au chatbot.")

    # Historique des interactions
    st.sidebar.subheader("Historique des interactions")
    if st.session_state.history:
        for entry in st.session_state.history:
            st.sidebar.markdown(f"**:blue[{entry['timestamp']}]**")
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
            st.sidebar.write("---")
    else:
        st.sidebar.info("Aucune interaction enregistrée pour le moment.")


# Exécuter l'application
if __name__ == "__main__":
    main()
