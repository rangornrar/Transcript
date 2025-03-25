from utils import logger

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from whisper_engine import transcrire, charger_modele
from openai_chat import envoyer_a_chatgpt, tester_api_key, enregistrer_api_key
from utils import install_missing_libraries, toggle_visibility

# 🌐 Variables globales d'état de l'IHM (remplies plus tard dans `construire_interface`)
champ_prompt = None
champ_reponse = None
api_status_label = None
toggle_button = None
liste_fichiers = None
texte_info = None
progress_bar = None
bouton_transcrire = None

def construire_interface(root, prefs):
    """
    Initialise l'interface graphique principale.
    Utilise les préférences sauvegardées pour préremplir les choix utilisateur.
    """

    # 🧠 Variables d'état liées à l'interface, associées au root
    global model_choice, language_choice, style_choice, decoupage_var, cuda_var, segment_length_var, api_key_var
    model_choice = tk.StringVar(master=root, value="large")
    language_choice = tk.StringVar(master=root, value="fr")
    style_choice = tk.StringVar(master=root, value="clam")
    decoupage_var = tk.BooleanVar(master=root)
    cuda_var = tk.BooleanVar(master=root)
    segment_length_var = tk.IntVar(master=root, value=30)
    api_key_var = tk.StringVar(master=root)

    install_missing_libraries()  # Vérifie les dépendances nécessaires

    # 📥 Application des préférences utilisateur
    model_choice.set(prefs.get("model", "large"))
    language_choice.set(prefs.get("language", "fr"))
    style_choice.set(prefs.get("theme", "clam"))
    cuda_var.set(prefs.get("cuda", False))
    decoupage_var.set(prefs.get("decoupage", False))
    segment_length_var.set(prefs.get("segment_duration", 30))
    api_key_var.set(prefs.get("apikey", ""))

    # 🎨 Configuration du style global de l'interface
    style = ttk.Style()
    style.theme_use(style_choice.get())

    root.title("🎙️ Transcripteur Whisper")
    root.geometry("1050x1000")

    # 🔐 Cadre d'entrée de la clé API
    frame_api = ttk.LabelFrame(root, text="🔐 Clé API OpenAI")
    frame_api.pack(padx=10, pady=10, fill='x')

    api_entry = ttk.Entry(frame_api, width=60, textvariable=api_key_var, show="*")
    api_entry.pack(side="left", padx=10, pady=5)

    api_status_label = ttk.Label(frame_api, text="")
    api_status_label.pack(side="left", padx=10)

    toggle_button = ttk.Button(frame_api, text="Afficher", command=lambda: toggle_visibility(api_entry, toggle_button))
    toggle_button.pack(side="left", padx=5)

    # Boutons pour tester ou enregistrer la clé API
    ttk.Button(frame_api, text="Tester", command=lambda: tester_api_key(api_entry, api_status_label)).pack(side="left", padx=5)
    ttk.Button(frame_api, text="Enregistrer", command=lambda: enregistrer_api_key(api_entry, api_status_label)).pack(side="left", padx=5)

    # 💬 Zone de prompt vers ChatGPT
    frame_chat = ttk.LabelFrame(root, text="💬 Envoi à ChatGPT")
    frame_chat.pack(padx=10, pady=10, fill='x')

    ttk.Label(frame_chat, text="Prompt à envoyer à l'API :").pack(padx=10, pady=5)

    champ_prompt = tk.Text(frame_chat, height=5)
    champ_prompt.pack(padx=10, pady=5, fill='x')

    champ_reponse = tk.Text(frame_chat, height=10)
    champ_reponse.pack(padx=10, pady=5, fill='x')

    # 📂 Section pour ajouter des fichiers audio
    frame_files = ttk.LabelFrame(root, text="📂 Sélection des fichiers audio")
    frame_files.pack(padx=10, pady=10, fill='x')

    liste_fichiers = tk.Listbox(frame_files, selectmode=tk.MULTIPLE, width=80, height=5)
    liste_fichiers.pack(pady=5, padx=10, fill='x')

    ttk.Button(
        frame_files,
        text="Sélectionner des fichiers audio",
        command=lambda: liste_fichiers.insert(
            tk.END,
            *filedialog.askopenfilenames(
                title="Sélectionner des fichiers audio",
                filetypes=[("Fichiers audio", "*.wav;*.mp3;*.m4a;*.flac")]
            )
        )
    ).pack(pady=5, padx=10)

    # 📝 Zone d'affichage de la progression de la transcription
    frame_output = ttk.LabelFrame(root, text="📝 État de la transcription")
    frame_output.pack(padx=10, pady=10, fill='both', expand=True)

    texte_info = tk.Text(frame_output, height=4, width=80)
    texte_info.pack(pady=5, padx=10, fill='both', expand=True)

    progress_bar = ttk.Progressbar(root, mode='determinate')
    progress_bar.pack(fill='x', pady=10, padx=10)

    bouton_transcrire = ttk.Button(
        root,
        text="Transcrire",
        command=lambda: transcrire(liste_fichiers, texte_info, progress_bar)
    )
    bouton_transcrire.pack(pady=10)

def get_etat_interface():
    """
    Récupère l’état actuel de l’IHM pour sauvegarde dans le fichier de configuration.
    """
    return {
        "model": model_choice.get(),
        "language": language_choice.get(),
        "theme": style_choice.get(),
        "cuda": cuda_var.get(),
        "decoupage": decoupage_var.get(),
        "segment_duration": segment_length_var.get(),
        "prompt": champ_prompt.get("1.0", "end").strip() if champ_prompt else "",
        "apikey": api_key_var.get().strip()
    }
