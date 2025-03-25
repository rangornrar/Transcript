import unittest
from unittest.mock import Mock, patch
from whisper_engine import transcrire

class TestWhisperEngine(unittest.TestCase):

    @patch("whisper.load_model")
    def test_transcrire(self, mock_load_model):
        model_mock = Mock()
        model_mock.transcribe.return_value = {"text": "Hello world"}
        mock_load_model.return_value = model_mock

        listbox = Mock()
        listbox.get.return_value = ["test.wav"]

        text = Mock()
        bar = Mock()

        with patch("builtins.open", unittest.mock.mock_open()) as mocked_file:
            transcrire(listbox, text, bar)
            mocked_file().write.assert_called_once_with("Hello world")