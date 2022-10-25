class Strain:
    """Represent the jth strain of the disease.
    :param die: death rate if individual is infected with jth strain
    :type die: float
    :param recover: recover rate if individual is infected with jth strain
    :type recover: float
    :param transmission: transmission rate of jth strain
    :type transmission: float
    :param infected: initial number of people infected with the strain
    :type infected: int
    """
    def __init__(self, alpha: float, nu: float, beta: float, infected: int):
        self.alpha = alpha
        self.nu = nu
        self.beta = beta
        self.infected = infected
        if not ((isinstance(alpha, float)) or (isinstance(alpha, int))):
            raise TypeError("Death rate should be float")
        if not ((isinstance(nu, float)) or (isinstance(nu, int))):
            raise TypeError("Recover rate should be float")
        if not ((isinstance(beta, float)) or (isinstance(beta, int))):
            raise TypeError("Transmission rate should be float")
        if not ((isinstance(infected, float)) or (isinstance(infected, int))):
            raise TypeError("Number of infected should be float")
