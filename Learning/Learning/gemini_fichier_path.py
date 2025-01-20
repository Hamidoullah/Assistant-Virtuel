# donne un fichier à gemini
import google.generativeai as gen_ai

# Configuration de l'API
GEN_API_KEY = "AIzaSyBmgCgeR2Ak4qZf8NItR-5j_VRsrrng-QY"
gen_ai.configure(api_key=GEN_API_KEY)

# Téléchargement du fichier PDF
sample_pdf = gen_ai.upload_file("D:/DiskD/download/BIG DATA/MPDS3/Frameworks Big Data/Mini-Projet/Documents/CoursCassandra1.pdf")

# Génération de contenu à partir du PDF
model = gen_ai.GenerativeModel(model_name="gemini-1.5-flash")
response = model.generate_content(["Donne-moi un résumé de ce fichier PDF.", sample_pdf])

print(response.text)