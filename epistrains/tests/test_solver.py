import unittest
from unittest.mock import patch
import epistrains as es
import pytest


class SolverTest(unittest.TestCase):
    """
    Tests the :class:`Solver` class.
    """

    def setUp(self):
        s1 = es.Strain(0.1, 0.2, 0.3, 10)
        s2 = es.Strain(0.1, 0.2, 0.6, 5)
        s3 = es.Strain(0.1, 0.2, 0.6, 1, delay=10)
        self.strains = [s1, s2, s3]
        br = es.make_br(2.0, 3.0)
        p = es.Population(0.5, 100, br)
        self.p = p

    def test_create(self):
        """
        Tests Solver creation.
        """
        s = es.Solver(strains=self.strains, pop=self.p)
        self.assertEqual(s.solution, None)

    def test_0_strains(self):
        with pytest.raises(ValueError):
            _ = es.Solver(strains=[], pop=self.p)

    def test_1_strain(self):
        s = es.Solver(strains=self.strains[:1], pop=self.p)
        s.solve()
        self.assertEqual(3, len(s.solution.y))

    def test_multiple_strain(self):
        s = es.Solver(strains=self.strains, pop=self.p)
        s.solve()
        self.assertEqual(5, len(s.solution.y))

    def test_count_virus_death(self):
        s = es.Solver(strains=self.strains, pop=self.p)
        with self.assertRaises(ValueError):
            s._count_virus_death()
        s.solve()
        s._count_virus_death()
        # check the length of the new death array
        self.assertEqual(len(s.deaths), len(s.solution.t))
        # check number deaths smaller than number of infected (at previous time step)
        assert(all(s.deaths[1:] <= (s.solution.y[1, :] + s.solution.y[2, :] + s.solution.y[3, :])[:-1]))

    def test_make_plot(self):
        s = es.Solver(strains=self.strains, pop=self.p)
        with self.assertRaises(ValueError):
            s._make_plot()
        s.solve()
        plt = s._make_plot()
        ax = plt.gca()
        # plot should have 5 lines: 1 S, 3 I, 1 R, 1 D
        self.assertEqual(len(ax.lines), 6)
        # all lines should be different
        for i in range(len(ax.lines)):
            for j in range(len(ax.lines)):
                if i != j:
                    assert(not all(ax.lines[i].get_ydata() == ax.lines[j].get_ydata()))

    def test_identical_strain(self):
        s = es.Solver(strains=[self.strains[0], self.strains[0]], pop=self.p)
        s.solve()
        plt = s._make_plot()
        ax = plt.gca()
        # identical strains should give identical lines
        assert(all(ax.lines[1].get_ydata() == ax.lines[2].get_ydata()))

    @patch('matplotlib.pylab.show')
    def test_plot(self, show):
        s = es.Solver(strains=self.strains, pop=self.p)
        s.solve()
        s.plot_compartments()
        assert show.called

    @patch('matplotlib.pylab.savefig')
    def test_save_plot(self, save):
        s = es.Solver(strains=self.strains, pop=self.p)
        s.solve()
        s.save_compartments('test.png')
        save.assert_called_with('test.png', dpi=300)
