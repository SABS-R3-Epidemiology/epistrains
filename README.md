[![Python application](https://github.com/SABS-R3-Epidemiology/epistrains/actions/workflows/python-app.yml/badge.svg)](https://github.com/SABS-R3-Epidemiology/epistrains/actions/workflows/python-app.yml)
[![codecov](https://codecov.io/gh/SABS-R3-Epidemiology/epistrains/branch/main/graph/badge.svg?token=UEYRNK9UE7)](https://codecov.io/gh/SABS-R3-Epidemiology/epistrains)
[![Documentation Status](https://readthedocs.org/projects/epistrains/badge/?version=latest)](https://epistrains.readthedocs.io/en/latest/?badge=latest)

# Epistrains

A multi-strain SIR model


## Installation

```
python install -e .
```

## Usage 

Below is an example of how use the package to define, solve and visualise the multi-strain SIR model. This model uses an exponential birth rate and models two strains with different recovery rates.

```python
from epistrains import Population, make_br, Strain, Solver, plot_compartments

birth_rate_function = make_br(a=100.0, k=3.0)

population = Population(death=0.05, size=1000, birth_function=birth_rate_function)

I1 = Strain(alpha=0.1, nu=0.1, beta=0.1, infected=5)
I2 = Strain(alpha=0.1, nu=0.3, beta=0.1, infected=3)

model = Solver(pop=poulation, strains=[I1, I2], time=10)
solution = model.solve()

plot_compartments(solution)
```

## Background

For this model, we assume that the total population size, N is governed by a population growth model with different birth rates but a constant per capita death rate. An example of this is as follows:
$$\frac{dN}{dt} = N\left(ae^{-kN}-b\right)$$
where \(a>b\). We can change this birth function to either uniform growth aN or logistic growth $aN\left(1-\frac{N}{k}\right)$ where k is the carrying capacity.  
The total population size obeys the following equation:
$$N = S + R + \sum_{j} I_j$$  
For our model we use a system of SIR ODEs with the following compartments: S (susceptible), R (recovered) or I\(_j\) (infected with thej\(^{th}\) strain of the disease). The ODEs that govern the time evolution of the system are:  
$$\frac{dN}{dt} = Nae^{-kN}-\sum_j \beta_j I_j S - bS$$

$$\frac{dI_j}{dt} = I_j(\beta_j S - (b + \nu_j + \alpha_j))$$

$$\frac{dR}{dt} = -bR + \sum_j \nu_j I_j$$

From these equations we can trivially check the equation for $\frac{dN}{dt}$.
