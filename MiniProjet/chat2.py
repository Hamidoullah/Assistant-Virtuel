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
DOC_DIR = "upload/documents"
os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(DOC_DIR, exist_ok=True)

mime_types_mapping = {
    "pdf": "application/pdf",
    "txt": "text/plain",
    "html": "text/html",
    "md": "text/markdown",
    "csv": "text/csv",
    "xml": "text/xml",
    "css": "text/css",
    "rtf": "text/rtf",
    "js": "text/javascript",
    "py": "text/x-python"
}

# Générer un nom de fichier unique basé sur l'horodatage
def generate_filename(original_name, directory):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    name, ext = os.path.splitext(original_name)
    filename = f"{timestamp}_{name}{ext}"
    return os.path.join(directory, filename), filename

# Fonction pour traiter les PDF
def generate_document_content(uploaded_file, question):
    file_extension = uploaded_file.name.split(".")[-1].lower()
    
    # Trouver le type MIME basé sur l'extension
    mime_type = mime_types_mapping.get(file_extension, "application/octet-stream")

    doc_bytes = uploaded_file.read()

    sample_doc = gen_ai.upload_file(
        io.BytesIO(doc_bytes),
        mime_type=mime_type
    )
    model = gen_ai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content([question, sample_doc])
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
    st.title("🚀 Application d'analyse multimédia utilisant l'IA générative : Chatbot, Analyse d'Images, et Analyse de documents avec Google Gemini 🤖")

    # Initialiser l'historique dans la session
    if "history" not in st.session_state:
        st.session_state.history = []

    # Vérifier si 'selected_entry' existe dans session_state, sinon l'initialiser
    if 'selected_entry' not in st.session_state:
        st.session_state.selected_entry = None  # Ou une autre valeur par défaut

    # affichage d'un logo dans la barre latérale    
    st.sidebar.image("logo.png", use_container_width=True)

    # Barre latérale pour le mode
    mode = st.sidebar.selectbox(
        "Choisissez une fonctionnalité :",
        ["Chatbot", "Analyse d'image", "Analyse de document"]
    )

    # Section : Analyse d'image
    if mode == "Analyse d'image":
        st.header("Analyse d'image 🖼️")
        uploaded_image = st.file_uploader("Chargez une image (formats acceptés : PNG, JPEG, WEBP, HEIC, HEIF)", 
                                          type=["png", "jpeg", "jpg", "webp", "heic", "heif"])
        user_question = st.text_input("Posez une question 🤔 sur l'image :")

        if st.button("Analyser l'image"):
            if uploaded_image and user_question:
                try:
                    # Sauvegarder l'image dans le répertoire upload/images
                    image_path, image_name = generate_filename(uploaded_image.name, IMAGE_DIR)

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
                        "file": image_name,
                        "question": user_question,
                        "response": response_text,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                except Exception as e:
                    st.error(f"Erreur lors du traitement de l'image : {str(e)}")
            else:
                st.warning("Veuillez charger une image avant d'analyser et poser une question.")

    # Section : Analyse de document
    elif mode == "Analyse de document":
        st.header("Analyse de document 📚")

        # Charger le fichier via Streamlit
        uploaded_file = st.file_uploader(
            "Chargez un document (formats acceptés : PDF, TXT, HTML, Markdown, CSV, XML, CSS, RTF, JavaScript, Python).",
            type=["pdf", "txt", "html", "md", "csv", "xml", "css", "rtf", "js", "py"]
        )
        user_question = st.text_input("Posez une question 🤔 sur le document :")

        if st.button("Analyser le document"):
            if uploaded_file and user_question:
                try:
                    # Sauvegarder le document dans le répertoire upload/documents
                    document_path, document_name = generate_filename(uploaded_file.name, DOC_DIR)

                    with open(document_path, "wb") as f:
                        f.write(uploaded_file.read())

                    response_text = generate_document_content(open(document_path, "rb"), user_question)

                    st.subheader("Réponse générée :")
                    st.write(response_text)

                    # Enregistrer l'interaction dans l'historique
                    st.session_state.history.insert(0, {
                        "type": "document",
                        "file": document_name,
                        "question": user_question,
                        "response": response_text,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                except Exception as e:
                    st.error(f"Erreur lors du traitement du document : {str(e)}")
            else:
                st.warning("Veuillez charger un fichier document et poser une question.")

    # Section : Chatbot simple
    elif mode == "Chatbot":
        st.header("Chatbot 💬")
        user_question = st.text_input("Posez une question 🤔 au chatbot :")
        
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

    # Affichage de l'historique dans la barre latérale
    st.sidebar.subheader("Historique des interactions")

    if st.session_state.history:
        for i, entry in enumerate(st.session_state.history):
            # Afficher toutes les interactions sans supprimer les anciennes
            st.sidebar.markdown(f"**:blue[{entry['timestamp']}]**")
            if entry["type"] == "image":
                    st.sidebar.write(f"- **Type :** Analyse d'image")
                    st.sidebar.write(f"- **Fichier :** {entry['file']}")
            elif entry["type"] == "document":
                st.sidebar.write(f"- **Type :** Analyse de document")
                st.sidebar.write(f"- **Fichier :** {entry['file']}")
            else:
                st.sidebar.write(f"- **Type :** Chatbot")
            # Afficher la question dans la sidebar, avec un découpage si elle dépasse 20 caractères
            question_text = entry['question']
            shortened_question = question_text[:20] + "..." if len(question_text) > 20 else question_text

            st.sidebar.write(f"- **Question :** {shortened_question}")

            # Utiliser un bouton pour chaque entrée de l'historique
            if st.sidebar.button(f"Voir détails", key=f"entry_{i}"):
                # Afficher les détails de l'interaction
                st.sidebar.write(f"- **Question :** {entry['question']}")
                st.sidebar.write(f"**Réponse:** {entry['response']}")
            st.sidebar.write("---")
    else:
        st.sidebar.info("Aucune interaction enregistrée pour le moment.")

# Exécuter l'application
if __name__ == "__main__":
    main()
