"""epistrains models a multi-strain SRI model
"""
# Import version info
from .version_info import VERSION_INT, VERSION  # noqa

# Import main classes
from .population import Population, make_br
from .strain import Strain
from .solver import Solver
