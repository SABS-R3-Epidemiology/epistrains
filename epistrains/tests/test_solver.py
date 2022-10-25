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
        br = es.make_br(2.0, 3.0)
        p = es.Population(0.5, 0, br)
        s = es.Solver(strains=[s1, s2], pop=p)
        self.assertEqual(s.solution, None)

    def test_1_strain(self):
        #Include len(strains) = 1
        s1 = es.Strain(0.1, 0.2, 0.3)
        br = es.make_br(2.0, 3.0)
        p = es.Population(0.5, 0, br)
        s = es.Solver(strains=[s1], pop=p)
        s.solve()
        self.assertEqual(3, len(s.solution))

    #def test_multiple_strain(self):
    #    s = es.Solver(strains,pop)
    #    s.solve()
    #    #Include len(strains) = 3
    #    self.assertEqual(5, len(s.solution))

