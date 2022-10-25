import unittest
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
        self.assertEqual(s.die, 0.1)
        self.assertEqual(s.recover, 0.2)
        self.assertEqual(s.transmission, 0.3)
