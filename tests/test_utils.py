import unittest
from unittest.mock import Mock
from utils import toggle_visibility

class TestUtils(unittest.TestCase):

    def test_toggle_visibility_masquer(self):
        entry = Mock()
        entry.cget.return_value = ""
        button = Mock()
        toggle_visibility(entry, button)
        entry.config.assert_called_with(show="*")
        button.config.assert_called_with(text="Afficher")

    def test_toggle_visibility_afficher(self):
        entry = Mock()
        entry.cget.return_value = "*"
        button = Mock()
        toggle_visibility(entry, button)
        entry.config.assert_called_with(show="")
        button.config.assert_called_with(text="Masquer")