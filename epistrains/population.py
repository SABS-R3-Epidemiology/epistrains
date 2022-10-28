import math


class Population:
    """
    Population based parameters for construction of birth and death rate terms
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
    :param waning: constant waning immunity rate
    :type waning: float
    :param immunity: percentage of population currently immune
    :type immunity: float
    """

    def __init__(self, death: float, size: int, birth_function=None, waning=0.0, immunity=0.0):
        """Initialize the class and take general population parameters relating to birth and death rates"""
        if not (isinstance(immunity, float) or isinstance(immunity, int)):
            raise TypeError("Immunity levels must be numeric")

        self.death_rate = death
        self.init_size = size
        self.birth_rate = birth_function
        self.waning_rate = waning
        self.current_immune = (immunity/100)*self.init_size

        if not isinstance(self.death_rate, float):
            raise TypeError("Death rate must be of type float")
        if not isinstance(self.init_size, int):
            raise TypeError("Initial population size must be of type int")
        if not isinstance(self.waning_rate, float):
            raise TypeError("Waning immunity rate must be of type float")


def make_br(a: float, k: float):
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
