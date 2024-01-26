import unittest
from ParserCoroutine import flatten, flatmap_parse, ParserMessage, ImmutablePainState
from SerialWrapper import read_serial
from mock import MagicMock
from serial import Serial
from GeneratorUtil import take, last, filterIsType


class SerialParserTest(unittest.TestCase):
    def setUp(self) -> None:
        self.serial = MagicMock(spec=Serial)

    def test_serial_mock(self):
        self.serial.read.return_value = b"test"
        self.assertEqual(b"test", self.serial.read())

    def test_basic_parse(self):
        expected = [ImmutablePainState()]
        self.serial.read.return_value = b"\0020\0000\0000\000"

        stream = read_serial(self.serial)
        stream = take(stream, 1)
        stream = flatten(stream)
        stream = flatmap_parse(stream)
        stream = filterIsType(stream, ImmutablePainState)

        result = list(stream)

        self.assertEqual(expected, result)
