from openai import OpenAI
from tkinter import messagebox
from utils import logger  # Pour journaliser les actions utilisateur/API

def envoyer_a_chatgpt(prompt_widget, response_widget, api_key):
    """
    Envoie le contenu du widget `prompt_widget` à l'API OpenAI ChatGPT.
    Affiche la réponse dans `response_widget`.

    Args:
        prompt_widget (tk.Text): Champ contenant le prompt à envoyer.
        response_widget (tk.Text): Zone d'affichage de la réponse.
        api_key (str): Clé API OpenAI à utiliser pour la requête.
    """
    prompt = prompt_widget.get("1.0", "end").strip()
    if not prompt:
        messagebox.showwarning("Prompt vide", "Veuillez entrer un prompt.")
        return

    response_widget.delete("1.0", "end")
    response_widget.insert("end", "⏳ Envoi en cours...")
    logger.info("Envoi du prompt à ChatGPT lancé.")

    try:
        client = OpenAI(api_key=api_key.strip())
        logger.debug("Client OpenAI initialisé.")

        # Appel à l'API ChatGPT avec le prompt utilisateur
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        reply = response.choices[0].message.content.strip()
        response_widget.delete("1.0", "end")
        response_widget.insert("end", reply)
        logger.info("Réponse reçue de ChatGPT.")

    except Exception as e:
        response_widget.delete("1.0", "end")
        response_widget.insert("end", f"❌ Erreur : {str(e)}")
        logger.error(f"Erreur lors de l'appel API : {e}")

def tester_api_key(entry, label):
    """
    Teste la validité de la clé API saisie.

    Args:
        entry (tk.Entry): Champ de saisie contenant la clé API.
        label (ttk.Label): Étiquette d'état à mettre à jour.
    """
    key = entry.get().strip()
    logger.info("Test de la clé API lancé.")

    if not key.startswith("sk-"):
        messagebox.showerror("Clé invalide", "❌ Clé invalide.")
        return

    try:
        client = OpenAI(api_key=key)
        client.models.list()  # On tente de lister les modèles pour valider la clé
        label.config(text="✅ Clé OK", foreground="green")
    except Exception as e:
        label.config(text="❌ Erreur", foreground="red")
        messagebox.showerror("Erreur API", str(e))

def enregistrer_api_key(entry, label):
    """
    Enregistre la clé API dans le fichier .env.

    Args:
        entry (tk.Entry): Champ contenant la clé API.
        label (ttk.Label): Étiquette de statut à mettre à jour.
    """
    key = entry.get().strip()
    from dotenv import set_key  # Import local pour éviter les dépendances inutiles si non utilisé
    logger.info("Enregistrement de la clé API lancé.")

    try:
        set_key(".env", "OPENAI_API_KEY", key)
        label.config(text="✅ Enregistrée", foreground="green")
    except Exception as e:
        label.config(text="❌ Erreur", foreground="red")
        logger.error(f"Erreur d'enregistrement : {e}")
