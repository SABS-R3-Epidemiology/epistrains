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
        s = es.Solver(strains = [es.Strain(0.1, 0.2, 0.3), es.Strain(0.1, 0.2, 0.3)])
        pass

    def test_solver(self):
        s = es.Solver(strains = [es.Strain(0.1, 0.2, 0.3), es.Strain(0.1, 0.2, 0.3)])
        self.assertEqual(len(s.solution), 0)
        # s.solver()
        # self.assertEqual(len(s.solution), 1)
