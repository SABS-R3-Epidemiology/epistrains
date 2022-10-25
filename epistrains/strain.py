class Strain:
    """Represent the jth strain of the disease.
    :param die: death rate if individual is infected with jth strain
    :type die: float
    :param recover: recover rate if individual is infected with jth strain
    :type recover: float
    :param transmission: transmission rate of jth strain
    :type transmission: float
    """
    def __init__(self, alpha: float, nu: float, beta: float):
        self.alpha = alpha
        self.nu = nu
        self.beta = beta
        if not ((isinstance(alpha, float)) or (isinstance(alpha, int))):
            raise TypeError("Death rate should be float")
        if not ((isinstance(nu, float)) or (isinstance(nu, int))):
            raise TypeError("Recover rate should be float")
        if not ((isinstance(beta, float)) or (isinstance(beta, int))):
            raise TypeError("Transmission rate should be float")
