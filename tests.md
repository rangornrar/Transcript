# ✅ Documentation des Tests Unitaires - Transcripteur Whisper

Ce fichier décrit les tests unitaires disponibles pour le projet **Transcripteur Whisper**, ainsi que les instructions pour les exécuter localement.

---

## 📁 Emplacement des tests

Les fichiers de test sont situés dans le dossier :

```
/tests
```

---

## 🔍 Fichiers de test

### `test_config.py`
- Vérifie que la sauvegarde et le chargement des préférences via `config.py` fonctionne.
- Utilise un `mock` de la fonction `get_etat_interface()` pour simuler les valeurs d’interface.

### `test_utils.py`
- Vérifie que la fonction `toggle_visibility()` affiche ou masque correctement le champ de clé API.
- Utilise des objets `Mock` pour simuler l’entrée (`Entry`) et le bouton (`Button`).

### `test_whisper_engine.py`
- Vérifie que la fonction `transcrire()` appelle correctement le modèle Whisper.
- Le modèle Whisper est **mocké** pour éviter un vrai traitement audio.
- Le test vérifie que le fichier `.txt` est écrit avec le texte transcrit simulé.

---

## Couverture actuelle
| Name                                               | Stmts | Miss | Cover |
|----------------------------------------------------|-------|------|-------|
| config.py                                          | 20    | 10   | 50%   |
| gui.py                                             | 66    | 49   | 26%   |
| openai_chat.py                                     | 46    | 40   | 13%   |
| tests\test_config.py                               | 25    | 5    | 80%   |
| tests\test_utils.py                                | 18    | 0    | 100%  |
| tests\test_whisper_engine.py                       | 16    | 0    | 100%  |
| utils.py                                           | 16    | 5    | 69%   |
| whisper_engine.py                                  | 20    | 2    | 90%   |
| -------------------------------------------------- |       |      |       |
| TOTAL                                              | 227   | 111  | 51%   |

## ▶️ Lancement des tests

### 1. Assurez-vous d’avoir les dépendances :

```bash
pip install -r requirements.txt
```

---

### 2. Lancez les tests avec `unittest` :

```bash
python -m unittest discover -s tests
```

---

### 3. Exemple de sortie attendue :

```
...
----------------------------------------------------------------------
Ran 3 tests in 0.45s

OK
```

---

## 🛠️ Conseils

- Les tests utilisent `unittest.mock` pour ne pas dépendre de l’interface réelle ni des appels réseau ou modèles lourds.
- Vous pouvez étendre les tests à l’IHM en ajoutant `pytest`, `pytest-mock` ou `pytest-tkinter`.

---

## 📌 À venir (améliorations possibles)

- Tests de la logique `openai_chat.py` avec `requests_mock`
- Couverture complète des interactions GUI avec `tkinter` simulé
- Intégration dans un pipeline CI (ex: GitHub Actions)
