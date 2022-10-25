import unittest
import epistrains as es
import numpy as np


class SolverTest(unittest.TestCase):
    """
    Tests the :class:`Solver` class.
    """
    def test_create(self):
        """
        Tests Solver creation.
        """
        s = es.Solver(strains = [es.Strain(0.1, 0.2, 0.3), es.Strain(0.1, 0.2, 0.3)],
        t_eval = np.linspace(0, self.time, int(self.time*10000)))
        pass

    def test_solver(self):
        s = es.Solver(strains = [es.Strain(0.1, 0.2, 0.3), es.Strain(0.1, 0.2, 0.3)])
        self.assertEqual(len(s.solution), 0)
        # s.solver()
        # self.assertEqual(len(s.solution), 1)
