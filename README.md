# 📖 README - Application de transcription audio avec Whisper + ChatGPT

## 🧰 Fonctionnalités principales

- Interface graphique moderne avec Tkinter
- Transcription audio avec [Whisper](https://github.com/openai/whisper)
- Support GPU (CUDA) et CPU
- Choix du modèle Whisper (tiny à large)
- Choix de la langue (fr, en, de)
- Découpage automatique en segments configurables (10s, 20s, 30s, 60s)
- Envoi automatique à ChatGPT avec prompt personnalisé
- Saisie et validation de la clé API OpenAI avec enregistrement dans `.env`
- Progression visuelle et retour utilisateur
- Compatible avec Windows, macOS, Linux

---

## ✅ Prérequis

- Python 3.10 ou plus
- FFmpeg installé et accessible dans le `PATH`
- Compte OpenAI et clé API valide (https://platform.openai.com/account/api-keys)

---

## 📦 Installation des dépendances

Tu peux lancer le script directement, il installe tout automatiquement. Sinon, tu peux pré-installer :

```bash
pip install torch torchaudio openai-whisper openai python-dotenv
```

---

## 🔐 Clé API OpenAI

- Saisis ta clé dans le champ prévu dans l'interface (menu Clé API)
- Le programme valide automatiquement la clé en la testant
- Elle est enregistrée dans `.env` sous la forme :

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 🧪 Accélération GPU (optionnelle)

Si tu as une carte NVIDIA compatible CUDA :

1. Installe [CUDA Toolkit](https://developer.nvidia.com/cuda-downloads)
2. Installe [cuDNN](https://developer.nvidia.com/cudnn)
3. Installe PyTorch avec CUDA (exemple avec CUDA 11.8) :

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

---

## ▶️ Lancement du programme

```bash
python transcript_v4.py
```

Lance l'application avec :
- Menu **Options** pour choisir :
  - Modèle Whisper
  - Langue
  - Thème graphique
  - Durée de segmentation
  - Activer/désactiver CUDA
- Zone de saisie du **prompt ChatGPT**
- Gestion directe de la **clé API** avec test et sauvegarde
- Zone de progression de transcription

---

## 💾 Transcription

- Le fichier audio est transcrit en `.txt`
- Il est utilisé automatiquement pour enrichir le prompt envoyé à ChatGPT

---

## 📤 Publication GitHub (optionnelle)

Utilise le script `publish_to_github.sh` ou `.bat` pour publier rapidement ton projet sur GitHub.

---

## 📄 Structure du projet

```text
transcript_v4.py             # Script principal
.env                         # Clé API OpenAI
Installation Guide Whisper.md  # Guide Markdown
publish_to_github.sh         # Publication Linux
publish_to_github_windows.bat # Publication Windows
```

---

## ❓ FAQ

- **Q : La transcription est lente** ?
  - A : Utilise CUDA avec un GPU ou choisis un modèle plus léger (tiny, base)

- **Q : Ma clé API ne fonctionne pas** ?
  - A : Assure-toi qu'elle commence par `sk-` et est bien valide dans OpenAI

- **Q : Peut-on choisir la durée des segments ?**
  - A : Oui, via le menu Options > Durée des segments

---

## 🧼 Désinstallation

```bash
pip uninstall torch torchaudio openai-whisper openai python-dotenv
```

---

## 🏁 Crédit

Ce projet utilise :
- [OpenAI Whisper](https://github.com/openai/whisper)
- [OpenAI ChatGPT API](https://platform.openai.com/docs/guides/gpt)
- [Tkinter GUI Toolkit](https://docs.python.org/3/library/tkinter.html)

---

Pour toute suggestion, contribution ou bug : ouvrez une issue ou contactez le développeur ✨
