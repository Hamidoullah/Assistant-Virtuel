1-Instructions pour créer et activer un environnement virtuel Python

    a-Créer l'environnement virtuel : Exécutez la commande suivante pour créer un nouvel environnement virtuel. 
    Remplacez mon_environnement par le nom que vous souhaitez donner à votre environnement :

        Sur Windows :
        python -m venv mon_environnement 



    b-Activer l'environnement virtuel :

        Sur Windows :
        mon_environnement\Scripts\activate



    c-désactiver l'environnement virtuel. 
        
        Sur Windows:
        deactivate



2-Instructions pour utiliser ce fichier requirements.txt :
Après avoir activé l'environnement virtuel(mon_environnement), installez les dépendances avec la commande suivante :

    Sur Windows :
    pip install -r requirements.txt


Pour la génération d'image : 
    Important :La version stable du SDK Python pour l'API Gemini n'est pas compatible avec Imagen.
    Au lieu d'installer le package google-generativeai à partir de PyPI, vous devez l'installer à partir de la branche GitHub imagen.

        Installez la dépendance à l'aide de pip:
            pip install -U git+https://github.com/google-gemini/generative-ai-python@imagen






