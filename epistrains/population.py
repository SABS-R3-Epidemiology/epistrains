import math

class Population:
    """
    Population based parameters for the construction of birth rate and death rate terms
    Parameters
    ----------
    death: float
        constant death rate
    a: float
        birth rate constant
    k: float
        birth rate exponent constant
    """

    def __init__(self, death, a, k):
        """Initialize the class and take general population parameters relating to birth and death rates"""
        self.death_rate = death
        self.birth_a = a
        self.birth_k = k

    def birth_rate(self, size):
        """Define exponential birth rate function
        Parameters
        ----------
        size: int
            total population size as calculated in model
        """
        rate = self.birth_a * math.exp(-self.birth_k * size)
        return rate
