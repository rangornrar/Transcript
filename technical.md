# 🧾 Documentation technique - Transcripteur Whisper + ChatGPT GUI

## 📌 Présentation

Cette application permet de :
- Transcrire des fichiers audio avec Whisper
- Choisir le modèle, la langue, le thème, l'utilisation de CUDA et la segmentation
- Envoyer la transcription à l'API OpenAI ChatGPT
- Gérer dynamiquement la clé API avec validation
- Interagir via une interface graphique moderne construite avec Tkinter

---

## 📁 Arborescence du projet

```
whisper_transcripteur_final/
├── transcript_v4.py              # Script principal
├── .env                          # Clé API sauvegardée
├── Installation Guide Whisper.md # Guide d'installation utilisateur
├── publish_to_github.sh          # Script de publication GitHub (Linux/macOS)
└── publish_to_github_windows.bat # Script de publication GitHub (Windows)
```

---

## 🧱 Dépendances Python

```python
REQUIRED_LIBRARIES = [
    "torch",
    "torchaudio",
    "openai-whisper",
    "openai",
    "python-dotenv",
    "tk"
]
```

Les dépendances sont automatiquement installées si absentes.

---

## 💡 Fonctions principales du script

### 🔹 `transcrire()`
Transcrit chaque fichier audio sélectionné. Si l'option découpage est active, l'audio est découpé en segments (durée personnalisable).

### 🔹 `charger_modele()`
Charge un modèle Whisper en fonction du choix utilisateur et du device (`cpu` ou `cuda`). Affiche les infos CUDA/GPU.

### 🔹 `envoyer_a_chatgpt()`
Prépare un prompt à partir du contenu du fichier transcrit et envoie la requête à l'API OpenAI (v1) via :
```python
from openai import OpenAI
client = OpenAI(api_key="...")
response = client.chat.completions.create(...)
```

### 🔹 `enregistrer_api_key()` et `tester_api_key()`
- Valident la syntaxe de la clé API (doit commencer par `sk-`)
- Testent la clé en appelant `client.Model.list()`
- En cas de succès, l'enregistrent dans `.env`

---

## 🖥️ Interface graphique Tkinter

### Menus dynamiques :
- **Modèle Whisper** : tiny à large
- **Langue** : fr, en, de
- **Thème** : tous les thèmes ttk disponibles
- **Découpage** : toggle + durée du segment (10/20/30/60s)
- **CUDA** : on/off

### Zones interactives :
- Sélection de fichiers audio
- Bouton Transcrire
- Zone de texte pour prompt
- Bouton Envoyer à ChatGPT
- Affichage de la réponse
- Champ API avec bouton **Afficher / Masquer**, **Tester**, **Enregistrer**

---

## 🔐 Fichier `.env`

Contient une seule ligne :
```
OPENAI_API_KEY=sk-XXXXXXXXXXXXXXXXXXXXXXXX
```

Ce fichier est lu au lancement du programme via `python-dotenv`.

---

## 🚀 Publication GitHub

### Linux/macOS : `publish_to_github.sh`
```bash
chmod +x publish_to_github.sh
./publish_to_github.sh
```

### Windows : `publish_to_github_windows.bat`
Double-cliquez simplement après avoir modifié l'URL GitHub dans le script.

---

## 📦 Création de l'exécutable

```bash
pip install pyinstaller
pyinstaller --onefile --windowed transcript_v4.py
```

L'exécutable sera disponible dans `dist/transcript_v4.exe`

---

## 🧪 Tests à prévoir

| Fonction | Testé | Résultat attendu |
|---------|--------|------------------|
| Chargement de modèles Whisper | ✅ | Affiche modèle et GPU |
| Découpage en segments | ✅ | Découpe et barre de progression |
| Transcription | ✅ | Génère .txt |
| ChatGPT | ✅ | Réponse affichée |
| API Key | ✅ | Clé valide, message ok |
| .env | ✅ | Clé stockée et relue |

---

## 🧼 Nettoyage

```bash
pip uninstall torch torchaudio openai-whisper openai python-dotenv
```

Supprimer aussi le dossier `.env`, `__pycache__/`, `dist/`, `build/` si nécessaire.

---

## ✨ Auteur

Ce projet a été généré avec amour et rigueur pour offrir une application complète, moderne, pratique et 100% personnalisable.

Pour toute suggestion, correction ou idée : [ouvrir une issue GitHub ou demander via l'app] 💬

