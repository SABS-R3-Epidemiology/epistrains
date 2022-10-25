class Strain:
    '''Represent the jth strain of the disease.
    :param die: death rate if individual is infected with jth strain
    :type die: float
    :param recover: recover rate if individual is infected with jth strain
    :type recover: float
    :param transmission: transmission rate of jth strain
    :type transmission: float
    '''
    def __init__(self, die: float, recover: float, transmission: float):
        self.die = die
        self.recover = recover
        self.transmission = transmission
