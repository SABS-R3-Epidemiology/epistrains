import unittest
import pytest
import epistrains as es


class StrainTest(unittest.TestCase):
    """
    Tests the :class:`Strain` class.
    """
    def test_create(self):
        """
        Tests Strain creation.
        """
        s = es.Strain(0.1, 0.2, 0.3, 10, 15)
        self.assertEqual(s.alpha, 0.5)
        self.assertEqual(s.nu, 5.0)
        self.assertEqual(s.beta_unscaled, 1.65)
        self.assertEqual(s.infected, 10)
        self.assertEqual(s.delay, 15)

        with pytest.raises(TypeError):
            s = es.Strain('bad', 0.2, 0.3, 10)

        with pytest.raises(TypeError):
            s = es.Strain(0.1, 'bad', 0.3, 10)

        with pytest.raises(TypeError):
            s = es.Strain(0.1, 0.2, 'bad', 10)

        with pytest.raises(TypeError):
            s = es.Strain(0.1, 0.2, 0.3, 10.5)

        with pytest.raises(TypeError):
            s = es.Strain(0.1, 0.2, 0.3, 10, 'bad')
