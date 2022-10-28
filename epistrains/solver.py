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
        self.deaths = None
        self.daily_cumulative_deaths = None
        self.n_sus = self.pop.init_size - sum(strain.infected for strain in self.strains) - self.pop.current_immune
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
        self.recovered = pop.current_immune
        self.func_birth = pop.birth_rate

    def _ODE_S(self, y, b):
        """First order derivative function for susceptible

        :param y: number of susceptible, infected and recovered individuals
        :type y: list
        :param b: death rate
        :type b: float
        """
        S = y[0]
        R = y[-1]
        sum_beta = sum((strain.beta_unscaled/self.n_sus)*y[i+1]
                       for i, strain in enumerate(self.strains))
        dS_dt = self.func_birth(int(sum(y))) - sum_beta*S - b*S + self.w*R
        return dS_dt

    def _ODE_I_j(self, y, b, j):
        """First order derivative function for jth strain

        :param y: number of susceptible, infected and recovered individuals
        :type y: list
        :param b: death rate
        :type b: float
        :param j: index of the infected strain
        :type j: int
        """
        dI_j_dt = y[j]*(self.beta_scaled[j-1]*y[0] - (b + self.nu[j-1]
                                                      + self.alpha[j-1]))
        return dI_j_dt

    def _ODE_R(self, y, b):
        """First order derivative function for recover

        :param y: number of susceptible, infected and recovered individuals
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

        :param y: number of susceptible, infected and recovered individuals
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
        y0 = np.array([self.n_sus] + [strain.infected for strain in self.strains] + [self.recovered])
        sol = scipy.integrate.solve_ivp(
            fun=lambda t, y: self._rhs(y),
            t_span=[t_eval[0], t_eval[-1]],
            y0=y0,
            t_eval=t_eval,
        )
        self.solution = sol

    def _count_virus_death(self):
        """Counting the number of deaths caused by the viruses
        """
        if self.solution is None:
            raise ValueError("Must run s.solve() before calculation deaths")

        output_solver = self.solution
        number_strains = output_solver.y.shape[0] - 2
        virus_death = np.repeat(0.0, len(output_solver.t))
        for i in range(1, number_strains+1):
            virus_death += np.array(output_solver.y[i, :]
                                    )*self.strains[i-1].alpha
        # virus death would be shown on next timestamp
        virus_death = np.append(np.array(0), virus_death[:-1])
        self.deaths = virus_death

    def _make_plot(self):
        """Creates the plot of the number of individuals
        in each compartment over time
        """
        if self.solution is None:
            raise ValueError("Must run s.solve() before plotting solutions")

        fig = plt.figure()
        output_solver = self.solution

        # Initialise colours and number of strains
        # number of strains equals #rows - S - R compartments
        number_strains = output_solver.y.shape[0] - 2
        colours_SRD = ["red", "blue", "brown"]
        colours_I = plt.cm.Greens(np.linspace(0.5, 1, number_strains))

        # Plot the S compartment
        plt.plot(output_solver.t, output_solver.y[0, :],
                 label="S", color=colours_SRD[0])

        # Plot the I compartments
        for i in range(1, number_strains+1):
            plt.plot(output_solver.t, output_solver.y[i, :],
                     label=f"I{i}", color=colours_I[i-1])

        # Plot the R compartment
        plt.plot(output_solver.t, output_solver.y[-1, :],
                 label="R", color=colours_SRD[1])

        # Plot number of deaths due to virus(es)
        self._count_virus_death()
        plt.plot(output_solver.t, self.deaths, label="D", color=colours_SRD[2])

        plt.legend()
        plt.ylabel("Number of individuals")
        plt.xlabel("Time (days)")
        plt.tight_layout()

        return fig

    def plot_compartments(self):
        """Function to show the compartments plot created by _make_plot
        """

        fig = self._make_plot()
        plt.show()

    def save_compartments(self, save_path='epistrains_output.png'):
        """Function to save the compartments plot created by _make_plot

        :param save_path: gives path to which figure should be saved
        :type save_path: string
        """

        fig = self._make_plot()
        plt.savefig(save_path, dpi=300)

    def _make_death_plot(self):
        """Creates the plot of the number of individuals
        in each compartment over time
        """
        if self.solution is None:
            raise ValueError("Must run s.solve() before plotting deaths")

        fig = plt.figure()
        output_solver = self.solution
        colours_deaths = ["midnightblue", "brown"]

        # plot daily deaths
        self._count_virus_death()
        plt.plot(output_solver.t, self.deaths, label="Daily", color=colours_deaths[1])

        plt.ylabel("Average number of deaths per day")
        plt.xlabel("Time (days)")
        ax = plt.gca()
        ax2 = ax.twinx()
        # plot cumulative deaths
        self.daily_cumulative_deaths = self.deaths.cumsum()/(len(output_solver.t)/(output_solver.t[-1]-output_solver.t[0]))
        ax2.plot(output_solver.t, self.daily_cumulative_deaths, label="Cumulative", color=colours_deaths[0])
        ax2.set_ylabel("Cumulative deaths", color=colours_deaths[0], fontsize=14)

        fig.legend(bbox_to_anchor=(0.8, 0.5))
        plt.tight_layout()

        return fig

    def plot_death(self):
        """Function to show the compartments plot created by _make_plot
        """
        fig = self._make_death_plot()
        plt.show()

    def save_death(self, save_path='epistrains_deaths_output.png'):
        """Function to save the compartments plot created by _make_plot

        :param save_path: gives path to which figure should be saved
        :type save_path: string
        """

        fig = self._make_death_plot()
        plt.savefig(save_path, dpi=300)
