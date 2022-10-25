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
    birth_function: lamda function, optional
        function to govern birth rate, defaults to exponential growth with a carrying capacity = (1/k)*log(a/b)
    """

    def __init__(self, death, a=None, k=None, birth_function=None):
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

        if birth_function is None:
            self.birth_function = birth_rate
        else:
            self.birth_funcction = birth_function
