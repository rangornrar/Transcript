
# 🧠 Documentation Technique — Transcripteur Whisper

Ce document décrit l'architecture, les modules et le fonctionnement général du projet **Transcripteur Whisper**, une application Python avec interface graphique pour la transcription audio via Whisper et l'intégration OpenAI.

---

## 📁 Structure du Projet

```
transcripteur_whisper/
│
├── main.py                 # Point d’entrée principal de l’application
├── gui.py                  # Interface graphique Tkinter
├── config.py               # Sauvegarde et chargement des préférences utilisateur
├── openai_chat.py          # Envoi de texte transcrit à l'API OpenAI (ChatGPT)
├── whisper_engine.py       # Transcription audio avec Whisper
├── utils.py                # Utilitaires : log, dépendances, masquage API
├── requirements.txt        # Dépendances Python
├── .env.example            # Exemple de fichier d’environnement avec clé API
├── README.md               # Documentation utilisateur
└── technical.md            # ⇨ CE FICHIER : Documentation technique
```

---

## ⚙️ main.py

- Crée la fenêtre principale avec `Tk()`
- Charge les préférences via `config.py`
- Appelle `construire_interface(...)`
- Déclenche `sauvegarder_preferences()` à la fermeture

---

## 🖼️ gui.py

- Construit toute l'interface utilisateur avec Tkinter :
  - Cadre API (clé OpenAI, test, enregistrement)
  - Zone d'envoi de prompt à ChatGPT
  - Liste de fichiers audio
  - Bouton de transcription
- Utilise les préférences chargées pour initialiser les champs
- Fournit `get_etat_interface()` pour permettre la sauvegarde

---

## 💾 config.py

- `charger_preferences()` : lit le fichier `.config_whisper_gui.json`
- `sauvegarder_preferences()` : écrit les paramètres depuis `gui.get_etat_interface()`
- Utilise `logger` pour tracer l'activité

---

## 🤖 openai_chat.py

- `envoyer_a_chatgpt(...)` :
  - Envoie un prompt à l’API ChatGPT
  - Affiche la réponse dans l’interface
- `tester_api_key(...)` : vérifie si une clé OpenAI est valide
- `enregistrer_api_key(...)` : stocke la clé dans le fichier `.env`

---

## 🔉 whisper_engine.py

- `transcrire(...)` :
  - Utilise le modèle Whisper pour transcrire chaque fichier audio sélectionné
  - Sauvegarde le texte transcrit dans un fichier `.txt`
- `charger_modele()` : charge le modèle Whisper de base

---

## 🧰 utils.py

- Initialise le système de log (`transcripteur.log`)
- `install_missing_libraries()` : installe automatiquement les dépendances manquantes
- `toggle_visibility()` : permet de masquer/afficher une entrée de type mot de passe (clé API)

---

## 🔐 Sécurité

- La clé API OpenAI est stockée localement dans un fichier `.env`
- L'interface masque la clé par défaut mais permet de l’afficher

---

## 📦 Dépendances

Listées dans `requirements.txt` :
- openai
- whisper
- torch
- torchaudio
- python-dotenv

---

## 📄 Fichier de configuration

- `.config_whisper_gui.json` contient :
  - modèle utilisé
  - langue
  - style de thème
  - durée des segments
  - préférence CUDA / découpage
  - dernier prompt saisi
  - clé API OpenAI

---

## 📈 Logs

- Tous les événements importants (transcription, envois API, erreurs...) sont enregistrés dans :
```
transcripteur.log
```

---

## 🏁 À faire / Idées d'amélioration

- Ajout d’une file d’attente pour les fichiers à transcrire
- Prévisualisation des transcriptions avant sauvegarde
- Choix du modèle Whisper directement dans l’interface
- Intégration d’un résumé automatique avec ChatGPT

---

## 🧠 Auteurs & Crédits

Projet initialement conçu pour permettre aux utilisateurs non techniques de transcrire leurs fichiers audio et d’utiliser l’intelligence artificielle simplement via une interface locale.
