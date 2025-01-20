import streamlit as st
import google.generativeai as gen_ai
import io

# Configuration de l'API
GEN_API_KEY = "AIzaSyBmgCgeR2Ak4qZf8NItR-5j_VRsrrng-QY"  # Remplacez par votre clé API
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
        
        # Demande à l'utilisateur une question
        user_question = st.text_input("Posez votre question :")
        
        if st.button("Obtenir la réponse") and user_question:
            # Génération de la réponse à partir du contenu du PDF et de la question
            with st.spinner("Chargement..."):
                response_text = generate_pdf_content(pdf_file, user_question)
                st.subheader("Réponse :")
                st.write(response_text)
    
if __name__ == "__main__":
    main()
