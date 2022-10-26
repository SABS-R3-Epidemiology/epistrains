import math


class Population:
    """
    Population based parameters for the construction of birth rate and death rate terms
    Parameters

    :param death: constant death rate
    :type death: float  
    :param size: initial population size
    :type size: int
    :param birth_function: function to govern birth rate
        exponential birth rate function created with make_br() can be used
        alternatively provide another function  in terms of N
        for a constant birth rate use: lambda N: constant
    :type birth_function: function
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

    :param a: birth rate constant
    :type a: float
    :param k: birth rate exponent constant
    :type k: float
    """
    if not isinstance(a, float):
        raise TypeError("Constant a must be of type float")
    if not isinstance(k, float):
        raise TypeError("Constant k must be of type float")

    def br(N: int):
        """Generate exponential birth rate function
        Parameters
        
        :param N: current population size
        :type N: int
        """
        if not isinstance(N, int):
            raise TypeError("Population size must be of type int")

        return N * a * math.exp(-k * N)
    return br
