import unittest
import epistrains as es


class SolverTest(unittest.TestCase):
    """
    Tests the :class:`Solver` class.
    """
    def test_create(self):
        """
        Tests Solver creation.
        """
        s1 = es.Strain(0.1, 0.2, 0.3)
        s2 = es.Strain(0.1, 0.2, 0.6)
        s = es.Solver(strains=[s1, s2])
        self.assertEqual(s.solution, None)
