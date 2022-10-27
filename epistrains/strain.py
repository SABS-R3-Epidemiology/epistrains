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
    def __init__(self, CFR: float, recovery_time: float, R0: float, infected: int):
        self.nu = 1/recovery_time
        self.alpha = CFR*self.nu
        self.beta_unscaled = (R0*(self.alpha + self.nu))
        self.infected = infected
        if not isinstance(CFR, float):
            raise TypeError("Case fatality rate should be float")
        if not isinstance(recovery_time, float):
            raise TypeError("Recovery time should be float")
        if not isinstance(R0, float):
            raise TypeError("R0 should be float")
        if not isinstance(infected, int):
            raise TypeError("Number of infected should be integer")
