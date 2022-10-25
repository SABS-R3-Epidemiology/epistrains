import unittest
import epistrains as es


class PopulationTest(unittest.TestCase):
    """
    Tests the :class:`Population` class.
    """
    def test_create(self):
        """
        Tests Population creation.
        """
        p = es.Population(100, 1, 1, 2)
        pass
