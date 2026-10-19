import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from config import charger_preferences, sauvegarder_preferences


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "preferences.json"
        self.patcher = patch("config.CONFIG_PATH", str(self.path))
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def test_sauvegarde_et_chargement(self):
        sauvegarder_preferences({"model": "small", "language": "en", "prompt": "Été"})
        self.assertEqual(charger_preferences(), {"model": "small", "language": "en", "prompt": "Été"})

    def test_cle_api_exclue_des_preferences(self):
        sauvegarder_preferences({"model": "small", "apikey": "secret-for-test"})
        self.assertNotIn("secret-for-test", self.path.read_text())
        self.assertEqual(json.loads(self.path.read_text()), {"model": "small"})

    def test_fichier_absent_ou_invalide(self):
        self.assertEqual(charger_preferences(), {})
        self.path.write_text("not json")
        self.assertEqual(charger_preferences(), {})
