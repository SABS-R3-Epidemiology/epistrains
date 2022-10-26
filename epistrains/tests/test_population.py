import unittest
import epistrains as es


class PopulationTest(unittest.TestCase):
    """
    Tests the :class:`Population` class.
    """
    def test_create(self):
        """
        Tests birth function is created with make_br()
        """
        br = es.make_br(2.0, 0.0)
        p = es.Population(0.5, 0, br)
        birth = p.birth_rate(10)
        self.assertEqual(20, birth)

    def test_input_birth(self):
        """
        Tests birth function can be specified
        """
        p = es.Population(0.5, 0, birth_function=lambda N: 5)
        birth = p.birth_rate(0)
        self.assertEqual(5, birth)

    def test_death_error(self):
        """
        Tests type error rasied for death rate input
        """
        with self.assertRaises(TypeError):
            es.Population(1, 0)

    def test_size_type(self):
        """
        Tests type error raised for initial population size
        """
        with self.assertRaises(TypeError):
            es.Population(0.5, 50.5)

    def test_make_br_error(self):
        """
        Tests type error raised for inputs to make_br()
        """
        with self.assertRaises(TypeError):
            es.make_br(2, 3.0)
        with self.assertRaises(TypeError):
            es.make_br(2.0, 3)

    def test_br_pop_size(self):
        """
        Tests type error raised when updating birth rate
        """
        br = es.make_br(2.0, 3.0)
        p = es.Population(0.5, 0, br)
        with self.assertRaises(TypeError):
            p.birth_rate(100.0)
