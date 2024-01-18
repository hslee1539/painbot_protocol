import unittest
from ParserCoroutine import *

class ParserCoroutineTest(unittest.TestCase):
    def setUp(self) -> None:
        return
    
    def test_wrong_data(self):
        data = b'\x00\x00'

        with ParserCoroutine() as parser:
            result = [parser.send(it) for it in data]

        self.assertEqual([ParserCoroutine.MESSAGE_FAIL] * 2, result)
    
    def test_simple_complete_data(self):
        data = b'\0020\0000\0000\000'
        expected = {
            "micro wave mode" : "continuous",
            "micro wave value": 0,
            "low frequency pulse mode"  : "continuous",
            "low frequency pulse value" : 0,
            "low frequency pulse pulse value" : "182Hz,500uS",
            "low frequency electric current" : 0
        }

        with ParserCoroutine() as parser:
            result = [parser.send(it) for it in data]

        self.assertEqual(expected, result[-1])
    


if __name__ == "__main__":
    unittest.main()