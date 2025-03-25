from utils import logger  # Logger pour journaliser les événements (démarrage, arrêt, erreurs...)

from tkinter import Tk  # Création de la fenêtre principale Tkinter
from gui import construire_interface  # Fonction de construction de l'IHM principale
from config import charger_preferences, sauvegarder_preferences  # Gestion des préférences utilisateur

def main():
    """
    Point d'entrée principal de l'application.
    Initialise la fenêtre Tkinter, charge les préférences, construit l'IHM,
    et démarre la boucle principale de l'application.
    """
    root = Tk()  # Création de la fenêtre principale
    prefs = charger_preferences()  # Chargement des préférences utilisateur sauvegardées
    construire_interface(root, prefs)  # Construction de l'IHM selon les préférences

    # Lors de la fermeture de la fenêtre, on sauvegarde les préférences avant de quitter
    root.protocol("WM_DELETE_WINDOW", lambda: (sauvegarder_preferences(), root.destroy()))

    root.mainloop()  # Boucle principale de l'IHM Tkinter

# Exécution du point d'entrée uniquement si ce fichier est lancé directement
if __name__ == "__main__":
    main()
