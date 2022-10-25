class Population:
    """
    Population based parameters for the construction of birth rate and death rate terms
    Parameters
    ----------
    size: int
        population size
    death: float
        constant death rate
    a: float
        birth rate constant
    k: float
        birth rate exponent constant
    """

    def __init__(self, size, death, a, k):
        """Initialize the class and take general population parameters relating to birth and death rates"""
        self.size = size
        self.death_rate = death
        self.birth_a = a
        self.birth_k = k
