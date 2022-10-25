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
        s = es.Solver(strains = [Strain(), Strain()])
        pass

    def test_solver(self):
        s = es.Solver(strains = [Strain(), Strain()])
        self.assertEqual(len(s.solution), 0)
        s.solve()
        self.assertEqual(len(s.solution), 1)
