import unittest
import epistrains as es
import pytest


class SolverTest(unittest.TestCase):
    """
    Tests the :class:`Solver` class.
    """
    def test_create(self):
        """
        Tests Solver creation.
        """
        s1 = es.Strain(0.1, 0.2, 0.3, 10)
        s2 = es.Strain(0.1, 0.2, 0.6, 5)
        br = es.make_br(2.0, 3.0)
        p = es.Population(0.5, 100, br)
        s = es.Solver(strains=[s1, s2], pop=p)
        self.assertEqual(s.solution, None)

    def test_0_strains(self):
        br = es.make_br(2.0, 3.0)
        p = es.Population(0.5, 100, br)
        with pytest.raises(ValueError):
            s = es.Solver(strains=[], pop=p)

    def test_1_strain(self):
        s1 = es.Strain(0.1, 0.2, 0.3, 10)
        br = es.make_br(2.0, 3.0)
        p = es.Population(0.5, 100, br)
        s = es.Solver(strains=[s1], pop=p)
        s.solve()
        self.assertEqual(3, len(s.solution.y))

    def test_multiple_strain(self):
        s1 = es.Strain(0.1, 0.2, 0.3, 10)
        s2 = es.Strain(0.1, 0.2, 0.6, 5)
        s3 = es.Strain(0.1, 0.2, 0.6, 1)
        br = es.make_br(2.0, 3.0)
        p = es.Population(0.5, 100, br)
        s = es.Solver(strains=[s1, s2, s3], pop=p)
        s.solve()
        self.assertEqual(5, len(s.solution.y))
