import math


class Population:
    """
    Population based parameters for the construction of birth rate and death rate terms
    Parameters
    ----------
    death: float
        constant death rate
    size: int
        initial population size
    birth_function: function
        function to govern birth rate
        exponential birth rate function created with make_br() can be used
        alternatively provide another function  in terms of N
        for a constant birth rate use: lambda N: constant
    """

    def __init__(self, death: float, size: int, birth_function=None):
        """Initialize the class and take general population parameters relating to birth and death rates"""
        self.death_rate = death
        self.init_size = size
        self.birth_rate = birth_function

        if not isinstance(self.death_rate, float):
            raise TypeError("Death rate must be of type float")
        if not isinstance(self.init_size, int):
            raise TypeError("Initial population size must be of type int")


def make_br(a, k):
    """Define exponential birth rate function
    Parameters
    ----------
    a: float
        birth rate constant
    k: float
        birth rate exponent constant
    """
    if not isinstance(a, float):
        raise TypeError("Constant a must be of type float")
    if not isinstance(k, float):
        raise TypeError("Constant k must be of type float")

    def br(N: int):
        """Generate exponential birth rate function
        Parameters
        ----------
        N: int
            current population size
        """
        if not isinstance(N, int):
            raise TypeError("Population size must be of type int")

        return N * a * math.exp(-k * N)
    return br
