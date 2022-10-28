class Strain:
    """Represent the jth strain of the disease.

    :param CFR: case fatality rate for jth strain
    :type CFR: float
    :param recovery_time: average number of days to recover from jth strain
    :type recovery_time: float
    :param R0: R0 value for jth strain
    :type R0: float
    :param infected: initial number of people infected with the strain
    :type infected: int
    """
    def __init__(self, CFR: float, recovery_time: float, R0: float,
                 infected: int):
        if not ((isinstance(CFR, float)) or (isinstance(CFR, int))):
            raise TypeError("Case fatality rate should be numeric")
        if not ((isinstance(recovery_time, float)) or
                (isinstance(recovery_time, int))):
            raise TypeError("Recovery time should be numeric")
        if not ((isinstance(R0, float)) or (isinstance(R0, int))):
            raise TypeError("R0 should be float")
        if not isinstance(infected, int):
            raise TypeError("Number of infected should be numeric")
        self.nu = 1/recovery_time
        self.alpha = CFR*self.nu
        self.beta_unscaled = (R0*(self.alpha + self.nu))
        self.infected = infected
