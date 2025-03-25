import subprocess
import sys
import whisper
import torch
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from dotenv import load_dotenv, set_key
load_dotenv()
from threading import Thread
import math
import openai

# Vérification et installation automatique des bibliothèques nécessaires
REQUIRED_LIBRARIES = ["torch", "torchaudio", "openai-whisper", "openai", "dotenv", "tk"]


def install_missing_libraries():
    for lib in REQUIRED_LIBRARIES:
        try:
            __import__(lib.replace("-", "_"))
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

install_missing_libraries()

# Clé API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY", "sk-...")

# Initialisation
root = tk.Tk()
root.title("🎙️ Transcripteur Whisper")
root.geometry("1050x900")

# Barre de menu
menubar = tk.Menu(root)
root.config(menu=menubar)

options_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Options", menu=options_menu)

style = ttk.Style()
style.theme_use('clam')
style.configure('TButton', font=('Arial', 10, 'bold'))
style.configure('TLabel', font=('Arial', 10))

model_choice = tk.StringVar(value="large")
language_choice = tk.StringVar(value="fr")
style_choice = tk.StringVar(value="clam")
decoupage_var = tk.BooleanVar()
cuda_var = tk.BooleanVar(value=torch.cuda.is_available())

# Fonctions pour le menu

def set_model(val):
    model_choice.set(val)

def set_language(val):
    language_choice.set(val)

def set_style(val):
    style_choice.set(val)
    style.theme_use(val)

def toggle_decoupage():
    decoupage_var.set(not decoupage_var.get())

def toggle_cuda():
    cuda_var.set(not cuda_var.get())

options_menu.add_cascade(label="Modèle Whisper", menu=tk.Menu(options_menu, tearoff=0))
model_menu = options_menu.children[list(options_menu.children)[-1]]
for m in ["tiny", "base", "small", "medium", "large"]:
    model_menu.add_radiobutton(label=m, variable=model_choice, value=m, command=lambda v=m: set_model(v))

options_menu.add_cascade(label="Langue", menu=tk.Menu(options_menu, tearoff=0))
language_menu = options_menu.children[list(options_menu.children)[-1]]
for l in ["fr", "en", "de"]:
    language_menu.add_radiobutton(label=l, variable=language_choice, value=l, command=lambda v=l: set_language(v))

options_menu.add_cascade(label="Thème", menu=tk.Menu(options_menu, tearoff=0))
theme_menu = options_menu.children[list(options_menu.children)[-1]]
for theme in style.theme_names():
    theme_menu.add_radiobutton(label=theme, variable=style_choice, value=theme, command=lambda v=theme: set_style(v))

options_menu.add_checkbutton(label="Activer découpage", variable=decoupage_var, command=toggle_decoupage)

segment_length_var = tk.IntVar(value=30)
segment_menu = tk.Menu(options_menu, tearoff=0)
for sec in [10, 20, 30, 60]:
    segment_menu.add_radiobutton(label=f"{sec} secondes", variable=segment_length_var, value=sec)
options_menu.add_cascade(label="Durée des segments", menu=segment_menu)
options_menu.add_checkbutton(label="Activer CUDA", variable=cuda_var, command=toggle_cuda)

# Cadre API ChatGPT
frame_api = ttk.LabelFrame(root, text="🔐 Clé API OpenAI")
frame_api.pack(padx=10, pady=10, fill='x')

api_key_var = tk.StringVar(value=os.getenv("OPENAI_API_KEY", ""))

api_entry = ttk.Entry(frame_api, width=60, textvariable=api_key_var, show="*")
api_entry.pack(side="left", padx=10, pady=5)

api_status_label = ttk.Label(frame_api, text="")
api_status_label.pack(side="left", padx=10)

def toggle_visibility():
    if api_entry.cget("show") == "":
        api_entry.config(show="*")
        toggle_button.config(text="Afficher")
    else:
        api_entry.config(show="")
        toggle_button.config(text="Masquer")

toggle_button = ttk.Button(frame_api, text="Afficher", command=toggle_visibility)
toggle_button.pack(side="left", padx=5)

def enregistrer_api_key():
    key = api_entry.get().strip()
    if not key.startswith("sk-") or len(key) < 20:
        messagebox.showerror("Clé invalide", "❌ Veuillez entrer une clé API valide commençant par 'sk-'")
        return
    api_status_label.config(text="🔄 Vérification de la clé...", foreground="blue")
    root.update()
    try:
        openai.api_key = key
        response = openai.Model.list()
        set_key(".env", "OPENAI_API_KEY", key)
        api_status_label.config(text="✅ Clé API valide et enregistrée", foreground="green")
        messagebox.showinfo("✅ Clé validée", "Votre clé API a été vérifiée et enregistrée avec succès.")
    except Exception as e:
        api_status_label.config(text="❌ Clé invalide", foreground="red")
        messagebox.showerror("Clé invalide", f"❌ Erreur lors de la vérification : {str(e)}")

    if not key.startswith("sk-") or len(key) < 20:
        messagebox.showerror("Clé invalide", "❌ Veuillez entrer une clé API valide commençant par 'sk-'")
        return
    try:
        openai.api_key = key
        response = openai.Model.list()
        set_key(".env", "OPENAI_API_KEY", key)
        messagebox.showinfo("✅ Clé validée", "Votre clé API a été vérifiée et enregistrée avec succès.")
    except Exception as e:
        messagebox.showerror("Clé invalide", f"❌ Erreur lors de la vérification : {str(e)}")

    if not key.startswith("sk-") or len(key) < 20:
        messagebox.showerror("Clé invalide", "❌ Veuillez entrer une clé API valide commençant par 'sk-'")
        return
    set_key(".env", "OPENAI_API_KEY", key)
    openai.api_key = key
    messagebox.showinfo("✅ Clé enregistrée", "Votre clé API a été enregistrée avec succès.")
ttk.Button(frame_api, text="Enregistrer", command=enregistrer_api_key).pack(side="left", padx=5)
ttk.Button(frame_api, text="Tester", command=lambda: tester_api_key(api_entry.get())).pack(side="left", padx=5)

frame_chat = ttk.LabelFrame(root, text="💬 Envoi à ChatGPT")
frame_chat.pack(padx=10, pady=10, fill='x')

label_prompt = ttk.Label(frame_chat, text="Prompt à envoyer à l'API :")
label_prompt.pack(padx=10, pady=5)
champ_prompt = tk.Text(frame_chat, height=5)
champ_prompt.pack(padx=10, pady=5, fill='x')

champ_reponse = tk.Text(frame_chat, height=10)
champ_reponse.pack(padx=10, pady=5, fill='x')

# Variable globale pour stocker le dernier fichier de transcription
derner_fichier_transcrit = None

def envoyer_a_chatgpt():
    global derner_fichier_transcrit
    prompt = champ_prompt.get("1.0", tk.END).strip()
    if not prompt:
        messagebox.showwarning("Prompt vide", "Veuillez entrer un prompt.")
        return

    if derner_fichier_transcrit and os.path.exists(derner_fichier_transcrit):
        with open(derner_fichier_transcrit, "r", encoding="utf-8") as f:
            contenu = f.read()
        prompt_complet = f"{prompt}\n\nContenu transcrit :\n{contenu}"
    else:
        prompt_complet = prompt

    champ_reponse.delete("1.0", tk.END)
    champ_reponse.insert(tk.END, "⏳ Envoi en cours...\n")
    root.update()
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt_complet}]
        )
        reply = response.choices[0].message.content.strip()
        champ_reponse.delete("1.0", tk.END)
        champ_reponse.insert(tk.END, reply)
    except Exception as e:
        champ_reponse.delete("1.0", tk.END)
        champ_reponse.insert(tk.END, f"❌ Erreur : {str(e)}")

btn_envoyer = ttk.Button(frame_chat, text="Envoyer à ChatGPT", command=envoyer_a_chatgpt)
btn_envoyer.pack(padx=10, pady=5)

# Cadre Fichiers
frame_files = ttk.LabelFrame(root, text="📂 Sélection des fichiers audio")
frame_files.pack(padx=10, pady=10, fill='x')

liste_fichiers = tk.Listbox(frame_files, selectmode=tk.MULTIPLE, width=80, height=5)
liste_fichiers.pack(pady=5, padx=10)

bouton_choisir = ttk.Button(frame_files, text="Sélectionner des fichiers audio", command=lambda: liste_fichiers.insert(tk.END, *filedialog.askopenfilenames(title="Sélectionner des fichiers audio", filetypes=[("Fichiers audio", "*.wav;*.mp3;*.m4a;*.flac")])) )
bouton_choisir.pack(pady=5, padx=10)

# Cadre Transcription
frame_output = ttk.LabelFrame(root, text="📝 État de la transcription")
frame_output.pack(padx=10, pady=10, fill='both', expand=True)

texte_info = tk.Text(frame_output, height=10, width=80)
texte_info.pack(pady=5, padx=10, fill='both', expand=True)

progress_bar = ttk.Progressbar(root, mode='determinate')
progress_bar.pack(fill='x', pady=10, padx=10)

# Chargement modèle
model = None
device = "cuda" if cuda_var.get() and torch.cuda.is_available() else "cpu"

def charger_modele():
    global model, device
    device = "cuda" if cuda_var.get() and torch.cuda.is_available() else "cpu"
    model_name = model_choice.get()
    model = whisper.load_model(model_name).to(device)
    texte_info.insert(tk.END, f"🚀 Modèle chargé : {model_name}\n")
    texte_info.insert(tk.END, f"CUDA activé : {'✅ Oui' if device == 'cuda' else '❌ Non'}\n")
    if device == 'cuda':
        gpu_name = torch.cuda.get_device_name(0)
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        texte_info.insert(tk.END, f"🖥️ GPU détecté : {gpu_name} ({gpu_memory:.2f} GB VRAM)\n")
    else:
        texte_info.insert(tk.END, "🖥️ GPU détecté : Aucun (utilisation du CPU uniquement)\n")

# Fonction transcription
def transcrire():
    charger_modele()
    fichiers = liste_fichiers.get(0, tk.END)
    if not fichiers:
        messagebox.showwarning("Aucun fichier", "Veuillez sélectionner au moins un fichier audio.")
        return

    bouton_transcrire.config(state=tk.DISABLED)

    def worker():
        global derner_fichier_transcrit
        lang = language_choice.get()
        for fichier in fichiers:
            nom_fichier = os.path.basename(fichier)
            nom_sortie = os.path.splitext(nom_fichier)[0] + ".txt"
            texte_info.insert(tk.END, f"📌 Transcription en cours : {nom_fichier}...\n")
            texte_info.update()
            start_time = time.time()
            if decoupage_var.get():
                audio = whisper.load_audio(fichier)
                duration = len(audio) / whisper.audio.SAMPLE_RATE
                chunk_length = segment_length_var.get()
                nb_chunks = math.ceil(duration / chunk_length)
                transcription_complete = ""
                for i in range(nb_chunks):
                    start_chunk = i * chunk_length
                    end_chunk = min(duration, (i + 1) * chunk_length)
                    audio_chunk = audio[int(start_chunk * whisper.audio.SAMPLE_RATE):int(end_chunk * whisper.audio.SAMPLE_RATE)]
                    result_chunk = model.transcribe(audio_chunk, language=lang, fp16=(device == 'cuda'), verbose=False)
                    transcription_complete += result_chunk["text"] + ""
                    progress_bar['value'] = ((i + 1) / nb_chunks) * 100
                    texte_info.update()
            else:
                result = model.transcribe(fichier, language=lang, fp16=(device == 'cuda'), verbose=False)
                transcription_complete = result["text"]
            transcription_complete = result["text"]
            with open(nom_sortie, "w", encoding="utf-8") as fichier_sortie:
                fichier_sortie.write(transcription_complete)
            temps_total = time.time() - start_time
            texte_info.insert(tk.END, f"✅ Terminé : {nom_fichier} ({temps_total:.2f}s)\n")
            texte_info.update()
            derner_fichier_transcrit = nom_sortie
        messagebox.showinfo("Terminé", "Toutes les transcriptions sont terminées !\n")
        bouton_transcrire.config(state=tk.NORMAL)

    Thread(target=worker).start()

bouton_transcrire = ttk.Button(root, text="Transcrire", command=transcrire)
bouton_transcrire.pack(pady=10)

root.mainloop()


def tester_api_key(possible_key):
    from tkinter import messagebox
    if not possible_key.startswith("sk-") or len(possible_key) < 20:
        messagebox.showerror("Clé invalide", "❌ Veuillez entrer une clé API valide commençant par 'sk-'")
        return
    api_status_label.config(text="🔄 Test de la clé...", foreground="blue")
    root.update()
    try:
        openai.api_key = possible_key
        response = openai.Model.list()
        api_status_label.config(text="✅ Clé API valide", foreground="green")
        messagebox.showinfo("✅ Clé OK", "Connexion à l'API OpenAI réussie.")
    except Exception as e:
        api_status_label.config(text="❌ Clé invalide", foreground="red")
        messagebox.showerror("Erreur API", f"❌ Erreur : {str(e)}")
