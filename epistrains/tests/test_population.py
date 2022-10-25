import unittest
import epistrains as es


class PopulationTest(unittest.TestCase):
    """
    Tests the :class:`Population` class.
    """
    def test_create(self):
        """
        Tests birth function.
        """
        p = es.Population(1, 2, 3)
        birth = p.birth_function(0)
        self.assertEqual(2, birth)

    def test_input_birth(self):
        """
        Tests birth function can be specified
        """
        p = es.Population(1, birth_function=5)
        birth = p.birth_function
        self.assertEqual(5, birth)
