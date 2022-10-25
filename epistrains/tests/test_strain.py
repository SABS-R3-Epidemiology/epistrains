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
        s = es.Strain(0.1, 0.2, 0.3)
        self.assertEqual(s.alpha, 0.1)
        self.assertEqual(s.nu, 0.2)
        self.assertEqual(s.beta, 0.3)

        with pytest.raises(TypeError):
            s = es.Strain('a', 0.2, 0.3)

        with pytest.raises(TypeError):
            s = es.Strain(0.1, [2, 3], 0.3)
