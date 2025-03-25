import logging

# 📋 Configuration du système de logs partagé
# Enregistre les logs dans un fichier 'transcripteur.log' et les affiche aussi dans la console
logging.basicConfig(
    level=logging.INFO,  # Niveau de log minimum (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s [%(levelname)s] %(message)s",  # Format des messages
    handlers=[
        logging.FileHandler("transcripteur.log"),   # Écrit les logs dans un fichier
        logging.StreamHandler()                     # Affiche les logs dans la console
    ]
)

# Logger global utilisable dans tous les modules
logger = logging.getLogger(__name__)

import subprocess, sys

def install_missing_libraries():
    """
    Vérifie si certaines bibliothèques indispensables sont installées.
    Si une bibliothèque manque, elle est automatiquement installée via pip.

    Cela garantit que l'utilisateur final dispose bien de toutes les dépendances
    nécessaires pour exécuter l'application.
    """
    for lib in ["torch", "torchaudio", "openai-whisper", "openai", "tk"]:
        try:
            __import__(lib.replace("-", "_"))  # Teste l'import
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])  # Installe si absent

def toggle_visibility(entry, button):
    """
    Alterne l'affichage de la clé API dans le champ `entry`.
    Utilisé pour masquer/afficher la clé API à l'utilisateur.

    Args:
        entry (tk.Entry): Champ de saisie contenant la clé API.
        button (ttk.Button): Bouton de bascule dont le texte doit changer.
    """
    if entry.cget("show") == "":
        entry.config(show="*")           # Masquer le texte
        button.config(text="Afficher")   # Modifier le texte du bouton
    else:
        entry.config(show="")            # Afficher le texte en clair
        button.config(text="Masquer")    # Modifier le texte du bouton
