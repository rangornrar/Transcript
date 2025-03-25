from utils import logger  # Logger centralisé pour traçabilité

import json
from os import path

# 📍 Chemin du fichier de configuration utilisateur
CONFIG_PATH = ".config_whisper_gui.json"

# 🔄 Chargement des préférences utilisateur au démarrage
logger.info('Chargement des préférences utilisateur.')
def charger_preferences():
    """
    Charge les préférences utilisateur depuis le fichier de configuration JSON.
    Si le fichier n'existe pas ou est invalide, retourne un dictionnaire vide.
    """
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

# 💾 Sauvegarde des préférences utilisateur à la fermeture de l'app
logger.info('Sauvegarde des préférences utilisateur.')
def sauvegarder_preferences():
    """
    Récupère l'état de l'interface graphique via `get_etat_interface`
    et enregistre les préférences utilisateur dans un fichier JSON.
    """
    from gui import get_etat_interface  # Import local pour éviter les import circulaires
    prefs = get_etat_interface()
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(prefs, f, indent=2)
    except Exception as e:
        print("Erreur lors de la sauvegarde des préférences :", e)
