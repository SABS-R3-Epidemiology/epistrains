from typing import List
import numpy as np
import scipy.integrate
from epistrains.population import Population
from epistrains.strain import Strain
import matplotlib.pylab as plt


class MultiSolver:
    """ MultiSolver based parameters for the construction of ODE 
    right hand equations. Calculate ODE solution and plot
    the results

    :param pop: population information relating to birth rate 
        and death rate
    :type pop: Population
    :param strains: a list of strains to be infected
    :type strains: List
    :param time: days over which the system should be solved for,
        defaults to 1
    :type time: float or integer, optional
    """
    def __init__(self, pop: Population, strains: List[Strain], time=1):
        """Initialize the class and take general solver parameters"""
        # number of strains 
        self.n = len(strains)
        self.n_comps = 2**len(strains)
        sus_comps = [set()]
        inf_comps = []
        for i in range(self.n):
            sus_with = [{i}.union(sus) for sus in sus_comps]
            sus_comps += sus_with
        for sus in sus_comps:
            for i in range(self.n):
                if i not in sus:
                    inf_comps.append((sus, i))
        self.sus_comps = sus_comps
        self.inf_comps = inf_comps
        self.all_comps = sus_comps + inf_comps
        self.time = round(time, 2)
        self.pop = pop
        self.strains = strains
        self.solution = None
        # should have at least one strain
        if self.n == 0:
            raise ValueError('Number of strains must be positive')
        # store a list of death rate(alpha), transmission rate(beta),
        # and recover rate(nu)
        self.alpha = []
        self.beta = []
        self.nu = []
        for strain in self.strains:
            self.alpha.append(strain.alpha)
            self.beta.append(strain.beta)
            self.nu.append(strain.nu)
        # store population related parameters
        self.b = pop.death_rate
        self.w = pop.waning_rate
        self.func_birth = pop.birth_rate

    def _comp_idx(self, label):
        """Return the index of the compartment for a list of included strains
        (i.e. _strain_idx({0, 1, 2}) returns 7 if there are 3 strains)

        :param label: a set of strains indexes which are included in the compartment
        :type label: set
        """
        idx = self.all_comps.index(label)
        return idx

    def _ODE_S(self, y, label):
        """First order derivative function for susceptible

        :param y: a list composed by susceptible, infected with j strains and recover
        :type y: list
        :param b: death rate
        :type b: float
        """
        I_in = []
        I_out = []
        for i in range(self.n):
            if i in label:
                I_in.append((label - {i}, i))
            else:
                I_out.append((label, i))
        dS_dt = 0
        sus_idx = self._comp_idx(label)
        for label in I_in:
            # Add infections clearing up
            strain = self.strains[label[1]]
            inf_idx = self._comp_idx(label)
            dS_dt += y[inf_idx]*strain.nu
        for label in I_out:
            # Remove new infections
            strain = self.strains[label[1]]
            inf_idx = self._comp_idx(label)
            I_comps = [inf_comp for inf_comp in self.inf_comps if inf_comp[1] == label[1]]
            inf_idxs = [self._comp_idx(inf_comp) for inf_comp in I_comps]
            has_I = [y[i] for i in inf_idxs]
            # dS_dt -= y[sus_idx]*y[inf_idx]*strain.beta
            dS_dt -= y[sus_idx]*sum(has_I)*strain.beta
        return dS_dt

    def _ODE_I(self, y, label):
        """First order derivative function for jth strain

        :param y: a list composed by susceptible, infected with j strains and recover
        :type y: list
        :param b: death rate
        :type b: float
        :param j: index of the infected strain
        :type j: int
        """
        strain = self.strains[label[1]]
        S_in = label[0]
        sus_idx = self._comp_idx(S_in)
        inf_idx = self._comp_idx(label)
        I_comps = [inf_comp for inf_comp in self.inf_comps if inf_comp[1] == label[1]]
        inf_idxs = [self._comp_idx(inf_comp) for inf_comp in I_comps]
        has_I = [y[i] for i in inf_idxs]
        dI_dt = y[sus_idx]*sum(has_I)*strain.beta - y[inf_idx]*strain.nu
        return dI_dt

    def _rhs(self, y):
        """Right hand equations for ODE solver

        :param y: a list composed by susceptible, infected with j strains and recover
        :type y: list
        """
        dy_sus = [self._ODE_S(y, label) for label in self.sus_comps]
        dy_inf = [self._ODE_I(y, label) for label in self.inf_comps]
        dy = dy_sus + dy_inf
        sus_idx = self._comp_idx(set())
        return dy

    def solve(self):
        """Solve the differential equations
        """
        t_eval = np.linspace(0, self.time, self.time*10)
        n_sus = self.pop.init_size - sum(strain.infected for strain in self.strains)
        # All combinations of susceptiblilty and infectivity
        y0 = np.array([0]*len(self.all_comps))
        # Susceptible to all infections
        sus_idx = self._comp_idx(set())
        y0[sus_idx] = n_sus
        for i in range(self.n):
            # Susceptible to all, infected with i
            inf_idx = self._comp_idx((set(), i))
            y0[inf_idx] = self.strains[i].infected
        sol = scipy.integrate.solve_ivp(
            fun=lambda t, y: self._rhs(y),
            t_span=[t_eval[0], t_eval[-1]],
            y0=y0,
            t_eval=t_eval,
        )
        self.solution = sol

    def _make_plot(self):
        """Creates the plot of the number of individuals in each compartment over time
        """

        if self.solution is None:
            raise ValueError("Must run s.solve() before plotting solutions")

        plt.figure()
        output_solver = self.solution

        # Initialise colours and number of strains
        number_strains = output_solver.y.shape[0] - 2  # number of rows in output minus the S and R compartments
        colours_SR = ["red", "blue"]
        colours_S = plt.cm.Reds(np.linspace(0.5, 1, len(self.sus_comps)))
        colours_I = plt.cm.Greens(np.linspace(0.5, 1, len(self.inf_comps)))

        # Plot the S compartments
        for i, sus_comp in enumerate(self.sus_comps):
            sus_idx = self._comp_idx(sus_comp)
            sus_label = '$S_{' + ','.join(str(idx) for idx in sus_comp) + '}$'
            # plt.plot(output_solver.t, output_solver.y[sus_idx, :], label=sus_label, color=colours_S[i])
            plt.plot(output_solver.t, output_solver.y[sus_idx, :], label=sus_label)

        # Plot the I compartments
        for i, inf_comp in enumerate(self.inf_comps):
            inf_idx = self._comp_idx(inf_comp)
            inf_label = '$S_{' + ','.join(str(idx) for idx in inf_comp[0]) + '}$ with ' + str(inf_comp[1])
            # plt.plot(output_solver.t, output_solver.y[inf_idx, :], label=inf_label, color=colours_I[i])
            plt.plot(output_solver.t, output_solver.y[inf_idx, :], label=inf_label)

        plt.legend()
        plt.ylabel("Number of individuals")
        plt.xlabel("Time (days)")

        return plt

    def plot_compartments(self):
        """Function to show the compartments plot created by _make_plot
        """

        plt = self._make_plot()
        plt.show()

    def save_compartments(self, save_path='epistrains_output.png'):
        """Function to save the compartments plot created by _make_plot
        
        :param save_path: gives path to which figure should be saved
        :type save_path: string
        """

        plt = self._make_plot()
        plt.savefig(save_path, dpi=300)
