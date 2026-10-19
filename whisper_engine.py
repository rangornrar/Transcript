import os
from utils import logger  # Logger centralisé pour journalisation

def transcrire(liste_fichiers, texte_info, progress_bar):
    """
    Lance la transcription de tous les fichiers audio sélectionnés dans l'IHM.
    Affiche l'état dans `texte_info`, met à jour la barre de progression `progress_bar`
    et sauvegarde chaque transcription dans un fichier texte.

    Args:
        liste_fichiers (tk.Listbox): Liste des fichiers audio sélectionnés.
        texte_info (tk.Text): Zone de texte pour afficher les logs de progression.
        progress_bar (ttk.Progressbar): Barre de progression de la transcription.
    """
    logger.info('Transcription démarrée.')

    # Chargement du modèle Whisper en mode "base"
    model = charger_modele()
    logger.debug('Modèle Whisper chargé.')

    fichiers = liste_fichiers.get(0, "end")  # Récupère tous les fichiers sélectionnés

    for fichier in fichiers:
        texte_info.insert("end", f"📌 Transcription : {fichier}\n")
        texte_info.update()

        # Transcription du fichier audio
        result = model.transcribe(fichier)

        # Écriture du texte transcrit dans un fichier .txt
        with open(os.path.splitext(fichier)[0] + ".txt", "w", encoding="utf-8") as f:
            f.write(result["text"])

        texte_info.insert("end", "✅ Terminé\n")
        texte_info.update()

        logger.info(f"Transcription effectuée pour : {fichier}")

def charger_modele():
    """
    Charge le modèle Whisper de niveau 'base'.
    Peut être utilisé pour une utilisation manuelle ou avancée.

    Returns:
        whisper.Whisper: Le modèle prêt à l'emploi.
    """
    logger.debug("Chargement du modèle Whisper (base)")
    import whisper
    return whisper.load_model("base")
