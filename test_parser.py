import unittest
from core_parser import *


class ParserCoroutineTest(unittest.TestCase):
    def setUp(self) -> None:
        return

    def test_wrong_data(self):
        data = b"\x00\x00"

        result = [ParserMessage.FAIL == it for it in flatmap_parse((it for it in data))]

        self.assertTrue(result)

    def test_simple_complete_data(self):
        data = b"\0020\0000\0000\000"
        expected = ImmutablePainState()

        stream = (it for it in data)
        for result in flatmap_parse(stream):
            pass

        self.assertEqual(expected, result)
    
    def test_end_data(self):
        data = b"\0020\0000\0000\000\003"
        expected = ImmutablePainState()

        stream = (it for it in data)
        for result in flatmap_parse(stream):
            pass

        self.assertEqual(expected, result)

    def test_error_data(self):
        data = b"\0020\0000\0000\000\000"
        expected = ParserMessage.FAIL

        stream = (it for it in data)
        for result in flatmap_parse(stream):
            pass

        self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()
