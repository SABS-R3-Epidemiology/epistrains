from typing import List
import numpy as np
import scipy.integrate
from epistrains.population import Population
from epistrains.strain import Strain
import matplotlib.pylab as plt


class Solver:
    """ Solver based parameters for the construction of ODE
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
        self.time = round(time, 2)
        self.pop = pop
        self.strains = strains
        self.solution = None
        self.n_sus = self.pop.init_size - sum(strain.infected for strain in self.strains)
        # should have at least one strain
        if self.n == 0:
            raise ValueError('Number of strains must be positive')
        # store a list of death rate(alpha), transmission rate(beta),
        # and recover rate(nu)
        self.alpha = []
        self.beta_scaled = []
        self.nu = []
        for strain in self.strains:
            self.alpha.append(strain.alpha)
            self.beta_scaled.append(strain.beta_unscaled/self.n_sus)
            self.nu.append(strain.nu)
        # store population related parameters
        self.b = pop.death_rate
        self.w = pop.waning_rate
        self.func_birth = pop.birth_rate

    def _ODE_S(self, y, b):
        """First order derivative function for susceptible

        :param y: a list composed by susceptible, infected with j strains and recover
        :type y: list
        :param b: death rate
        :type b: float
        """
        S = y[0]
        R = y[-1]
        sum_beta = sum((strain.beta_unscaled/self.n_sus)*y[i+1] for i, strain in enumerate(self.strains))
        dS_dt = self.func_birth(int(sum(y))) - sum_beta*S - b*S + self.w*R
        return dS_dt

    def _ODE_I_j(self, y, b, j):
        """First order derivative function for jth strain

        :param y: a list composed by susceptible, infected with j strains and recover
        :type y: list
        :param b: death rate
        :type b: float
        :param j: index of the infected strain
        :type j: int
        """
        dI_j_dt = y[j]*(self.beta_scaled[j-1]*y[0] - (b + self.nu[j-1] + self.alpha[j-1]))
        return dI_j_dt

    def _ODE_R(self, y, b):
        """First order derivative function for recover

        :param y: a list composed by susceptible, infected with j strains and recover
        :type y: list
        :param b: death rate
        :type b: float
        """
        R = y[-1]
        sum_nu = 0
        for i in range(1, self.n+1):
            sum_nu += self.nu[i-1]*y[i]
        dR_dt = -b*R + sum_nu - self.w*R
        return dR_dt

    def _rhs(self, y):
        """Right hand equations for ODE solver

        :param y: a list composed by susceptible, infected with j strains and recover
        :type y: list
        """
        dy = [self._ODE_S(y, self.b)]
        for i in range(1, self.n+1):
            dy.append(self._ODE_I_j(y, self.b, i))
        dy.append(self._ODE_R(y, self.b))
        return dy

    def solve(self):
        """Solve the differential equations
        """
        t_eval = np.linspace(0, self.time, self.time*10)
        y0 = np.array([self.n_sus] + [strain.infected for strain in self.strains] + [0.0])
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
        colours_I = plt.cm.Greens(np.linspace(0.5, 1, number_strains))

        # Plot the S compartment
        plt.plot(output_solver.t, output_solver.y[0, :], label="S", color=colours_SR[0])

        # Plot the I compartments
        for i in range(1, number_strains+1):
            plt.plot(output_solver.t, output_solver.y[i, :], label=f"I{i}", color=colours_I[i-1])

        # Plot the R compartment
        plt.plot(output_solver.t, output_solver.y[-1, :], label="R", color=colours_SR[1])

        plt.legend()
        plt.ylabel("Number of individuals")
        plt.xlabel("Time (days)")
        plt.tight_layout()

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
