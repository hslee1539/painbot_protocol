from main import Serial, model, use_case, repository
import unittest
from mock import MagicMock


class MainTest(unittest.TestCase):
    def setUp(self) -> None:
        self.serial = MagicMock(spec=Serial)
    def test_empty(self):
        expected = []
        self.serial.read.return_value = b''

        for result in model(use_case(repository(self.serial))): break
        
        self.assertEquals(expected, list(result))
        