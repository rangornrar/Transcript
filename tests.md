# Tests unitaires — Transcript

Les tests sont dans `tests/` et s'exécutent avec `unittest`. Ils isolent le moteur audio et l'interface : aucun GPU, modèle Whisper téléchargé ni appel API n'est nécessaire.

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

GitHub Actions lance ces tests, puis `python -m compileall -q .`, à chaque envoi et pull request (`.github/workflows/`).

## Contenu (7 tests)

### `test_config.py`
- `test_sauvegarde_et_chargement` : les préférences enregistrées par `config.py` sont relues à l'identique.
- `test_cle_api_exclue_des_preferences` : la clé API n'est pas écrite dans le fichier de préférences.
- `test_fichier_absent_ou_invalide` : un fichier de préférences absent ou illisible ne bloque pas le chargement.

### `test_utils.py`
- `test_toggle_visibility_masquer` / `test_toggle_visibility_afficher` : `toggle_visibility()` masque ou affiche le champ de clé API (widgets simulés par `Mock`).

### `test_whisper_engine.py`
- `test_transcrire_ecrit_utf8_sans_modifier_audio` : `transcrire()` écrit le texte en UTF-8 sans toucher au fichier audio (modèle Whisper simulé).
- `test_plusieurs_fichiers_produisent_des_sorties_distinctes` : chaque fichier audio produit son propre fichier texte.

## Non couvert

- L'interface Tkinter réelle (`gui.py`) et le parcours de l'appel API (`openai_chat.py`).
- Une transcription réelle avec Whisper : à vérifier manuellement.
