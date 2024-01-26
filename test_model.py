import unittest
from core_model import *


class PlotModelTest(unittest.TestCase):
    def test_single_data(self):
        expected = [PlotState([0], [0], (0, 100))]

        stream = (ImmutablePainState() for i in range(1))
        result = plot_model(stream)

        self.assertEquals(expected, list(result))

    def test_two_data(self):
        expected = [PlotState([0], [0], (0, 100)), PlotState([0, 1], [0, 0], (0, 100))]

        stream = (ImmutablePainState() for i in range(2))
        result = plot_model(stream)

        self.assertEquals(expected, list(result))

    def test_overflow(self):
        expected = PlotState(list(range(900, 1000)), [0] * 100, (0, 100))

        stream = (ImmutablePainState() for i in range(1000))
        for result in plot_model(stream): continue

        self.assertEqual(expected, result)
