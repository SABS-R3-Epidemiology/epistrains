from typing import List
import numpy as np
import scipy.integrate
from epistrains.strain import Strain
import matplotlib.pylab as plt


class Solver:
    """:param strains: a list of strains to be infected
    :type strains: _type_
    :param t_eval: a list of arguments for start time,
        end time and time interval
    :type t_eeval: list
    :param time: timeframe (h) over which the models should be solved for,
        defaults to 1
    :type time: float, optional
    """
    def __init__(self, pop, strains: List[Strain], time=1):
        self.n = len(strains)
        self.time = round(time, 2)
        self.pop = pop
        self.strains = strains
        self.solution = None
        if self.n <= 0:
            raise ValueError('Number of strains must be positive')
        self.strains = strains
        self.alpha = []
        self.beta = []
        self.nu = []
        for strain in self.strains:
            self.alpha.append(strain.alpha)
            self.beta.append(strain.beta)
            self.nu.append(strain.nu)

        self.b = pop.death_rate
        self.func_birth = pop.birth_rate

    def _ODE_S(self, y, b):
        sum_beta = sum(strain.beta*y[i+1] for i, strain in enumerate(self.strains))
        dS_dt = self.func_birth(int(sum(y))) - sum_beta*y[0] - b*y[0]
        return dS_dt

    def _ODE_I_j(self, y, b, j):
        dI_j_dt = y[j]*(self.beta[j-1]*y[0] - (b + self.nu[j-1] + self.alpha[j-1]))
        return dI_j_dt

    def _ODE_R(self, y, b):
        sum_nu = 0
        for i in range(1, self.n+1):
            sum_nu += self.nu[i-1]*y[i]
        dR_dt = -b * y[-1] + sum_nu
        return dR_dt

    def _rhs(self, y):
        dy = [self._ODE_S(y, self.b)]
        for i in range(1, self.n+1):
            dy.append(self._ODE_I_j(y, self.b, i))
        dy.append(self._ODE_R(y, self.b))
        return dy

    def solve(self):
        """Solve the differential equations of the system
        """
        t_eval = np.linspace(0, self.time, int(self.time*100))
        n_sus = self.pop.init_size - sum(strain.infected for strain in self.strains)
        y0 = np.array([n_sus] + [strain.infected for strain in self.strains] + [0.0])
        sol = scipy.integrate.solve_ivp(
            fun=lambda t, y: self._rhs(y),
            t_span=[t_eval[0], t_eval[-1]],
            y0=y0,
            t_eval=t_eval,
        )
        self.solution = sol

    def plot_compartments(self, save_path=False):
        """Function to plot the counts in the compartments over time
        :param save_path: gives path to which figure should be saved. Default is False, figure would not be saved.
        :type time: string, boolean
        """

        fig = plt.figure()
        output_solver = self.solution

        #initialise colours and number of strains
        number_strains = output_solver.y.shape[0] - 2 #number of rows in output minus the S and R compartments
        colours_SR = ["red", "blue"]
        colours_I = plt.cm.summer(np.linspace(0, 1, number_strains))

        #plot the S and R compartment
        plt.plot(output_solver.t, output_solver.y[0, :], label="S", color = colours_SR[0])
        plt.plot(output_solver.t, output_solver.y[-1, :], label="R", color = colours_SR[1])

        #plot the I compartments
        for i in range(1,number_strains+1):
            plt.plot(output_solver.t, output_solver.y[i, :], label=f"I{i}", color = colours_I[i-1])

        plt.legend()
        plt.ylabel("Number of individuals")
        plt.xlabel("Time (days)")

        #save figure if required
        if save_path:
            plt.savefig(save_path)

        plt.show()
