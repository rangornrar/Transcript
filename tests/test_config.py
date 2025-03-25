import unittest
import json
import os
from config import charger_preferences, sauvegarder_preferences, CONFIG_PATH

class TestConfig(unittest.TestCase):

    def setUp(self):
        self.backup = None
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                self.backup = f.read()

    def tearDown(self):
        if self.backup is not None:
            with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
                f.write(self.backup)
        elif os.path.exists(CONFIG_PATH):
            os.remove(CONFIG_PATH)

    def test_sauvegarde_et_chargement(self):
        # Fake interface data
        from types import SimpleNamespace
        import builtins
        from gui import get_etat_interface

        builtins.get_etat_interface = lambda: {
            "model": "small",
            "language": "en",
            "theme": "default",
            "cuda": False,
            "decoupage": False,
            "segment_duration": 15,
            "prompt": "Test prompt",
            "apikey": "sk-test"
        }

        sauvegarder_preferences()
        prefs = charger_preferences()
        self.assertEqual(prefs["model"], "small")
        self.assertEqual(prefs["language"], "en")