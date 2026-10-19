import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch
from whisper_engine import transcrire


class TestWhisperEngine(unittest.TestCase):
    @patch("whisper_engine.charger_modele")
    def test_transcrire_ecrit_utf8_sans_modifier_audio(self, load_model):
        load_model.return_value.transcribe.return_value = {"text": "Été à Lias"}
        with tempfile.TemporaryDirectory() as directory:
            audio = Path(directory) / "test.wav"
            audio.write_bytes(b"original")
            files = Mock()
            files.get.return_value = [str(audio)]
            transcrire(files, Mock(), Mock())
            self.assertEqual(audio.with_suffix(".txt").read_text(encoding="utf-8"), "Été à Lias")
            self.assertEqual(audio.read_bytes(), b"original")
            load_model.return_value.transcribe.assert_called_once_with(str(audio))

    @patch("whisper_engine.charger_modele")
    def test_plusieurs_fichiers_produisent_des_sorties_distinctes(self, load_model):
        load_model.return_value.transcribe.side_effect = [{"text": "one"}, {"text": "two"}]
        with tempfile.TemporaryDirectory() as directory:
            paths = [str(Path(directory) / name) for name in ("one.wav", "two.mp3")]
            files = Mock()
            files.get.return_value = paths
            transcrire(files, Mock(), Mock())
            self.assertEqual([Path(name).with_suffix(".txt").read_text() for name in paths], ["one", "two"])
