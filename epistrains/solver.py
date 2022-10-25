from typing import List
import numpy as np
import scipy.integrate
from epistrains.strain import Strain

class Solver:
    """
    :param strains: a list of strains to be infected
    :type strains: _type_
    :param time: timeframe (h) over which the models should be solved for, 
        defaults to 1
    :type time: float, optional
    """
    def __init__(self, strains: List[Strain], time = 1):
        self.time = round(time, 2)
        self.solution = []
        self.strains = strains
   

    def solver(self):
        """Solve the differential equations
        """
        t_eval = np.linspace(0, self.time, int(self.time*10000))
        y0 = np.array([0.0, 0.0] + [0.0 for _ in self.strains])
        sol = scipy.integrate.solve_ivp(
            fun = lambda t, y: self.ODE(t, y, ), #finish by Nathan's fun name
            t_span = [t_eval[0], t_eval[-1]],
            y0 = y0,
            t_eval = t_eval,
            max_step = 0.001
        )
        self.solution = sol
