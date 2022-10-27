[![Python application](https://github.com/SABS-R3-Epidemiology/epistrains/actions/workflows/python-app.yml/badge.svg)](https://github.com/SABS-R3-Epidemiology/epistrains/actions/workflows/python-app.yml)
[![Run on multiple OS](https://github.com/SABS-R3-Epidemiology/epistrains/actions/workflows/os-tests.yml/badge.svg)](https://github.com/SABS-R3-Epidemiology/epistrains/actions/workflows/os-tests.yml)
[![codecov](https://codecov.io/gh/SABS-R3-Epidemiology/epistrains/branch/main/graph/badge.svg?token=UEYRNK9UE7)](https://codecov.io/gh/SABS-R3-Epidemiology/epistrains)
[![Documentation Status](https://readthedocs.org/projects/epistrains/badge/?version=latest)](https://epistrains.readthedocs.io/en/latest/?badge=latest)

# Epistrains

A multi-strain SIR model


## Installation

```
python install -e .
```

## Usage

Below is an example of how use the package to define, solve and visualise the multi-strain SIR model. This model uses the default birth rate and models two strains with different death, recovery, and transmission rates, along with a different number of individuals initially infected with each strain. This code can also be found in `example.py`

Import the relevant classes and functions from the epistrains package.
```python
from epistrains import Population, make_br, Strain, Solver
```
Generate a birth rate function with exponential form: $Nae^{-kN}$
``` python
birth_rate_function = make_br(a=10.0, k=0.001)
```
Instantiate the population class with a death rate = 0.000006, and initial population size = 150,000 and the exponential birth rate function defined above.
``` python
population = Population(death=0.000006, size=150000, birth_function=birth_rate_function)
```
Generate two strains to model. Strain I1 has a case fatality rate (CFR) = 0.00007, recovery time = 7 days, and an R0 = 3.14. At the start of the simulation 150 individuals are infected with strain I1. Strain I2 has a case fatality rate (CFR) = 0.001, recovery time = 8 days, and an R0 = 4.22. At the start of the simulation 10 individuals are infected with strain I2.
R0 is the basic reproduction number and represents the average number of cases of an infectious disease that arise by transmission from a single infected individual.
```python
I1 = Strain(CFR=0.00007, recovery_time=7, R0=3.14, infected=150)
I2 = Strain(CFR=0.001, recovery_time=8, R0=4.22, infected=10)
```
Instantiate the Solver class, providing it with the population structure and the two strains to be modelled, as well as the total time over which to run the simulation.
```python
model = Solver(pop=population, strains=[I1, I2], time=70)
```
Solve the set of equations for the 4 compartments and plot the results to be displayed and saved. To save the plot, provide the path denoting where to save the plot to `save_compartments()`.
```python
model.solve()
model.plot_compartments()
model.save_compartments('epistrains_example.png')
```

It is also possible to implement an alternative birth rate function instead of the default exponential. For example:
```python
population = Population(death=0.000006, size=150000, birth_function= lambda N: 0.0005*N)
```
![Example output](https://github.com/SABS-R3-Epidemiology/epistrains/blob/6c47b375c1a6fdcead70151ad30822c45a5f1735/epistrains_example.png =100x20)

## Background

SIR models are a form of compartment model used for the mathematical modelling of infectious disease. Here, we implement the model developed by Bremermann and Thieme (1989)[^1], in which there are multiple infected compartments, one for each strain.

We assume that the total population size, $N$ is governed by a population growth model with a per capita exponential birth rate by default and a constant per capita death rate. This is represented as follows:
$$\frac{dN}{dt} = N\left(ae^{-kN}-b\right)$$
where $a$ and $k$ are constants of the exponential birth function, $b$ is the per capita death rate, and $\(a>b\)$ such that the carrying capacity of the population is $\frac{1}{k}\log(\frac{a}{b})$. This birth function can be changed by the user, for example to uniform growth $aN$ or logistic growth $aN\left(1-\frac{N}{k}\right)$ where $k$ is the carrying capacity.  

The total population size obeys the following equation:
$$N = S + R + \sum_{j} I_j$$  
where $S$ is the number of susceptible individuals, $R$ is the number of recovered individuals, and $I\(_j\)$ is the number of individuals infected with strain $j$.
Therefore, for our model we use a system of SIR ODEs with the following compartments: $S$ (susceptible), $R$ (recovered) or $I_j$ (infected with the $j^{th}$ strain of the disease). The ODEs that govern the time evolution of the system are:  
$$\frac{dS}{dt} = Nae^{-kN}-\sum_j \beta_j I_j S - bS$$

$$\frac{dI_j}{dt} = I_j(\beta_j S - (b + \nu_j + \alpha_j))$$

$$\frac{dR}{dt} = -bR + \sum_j \nu_j I_j$$

where $a$ and $k$ are parameters relating to the exponential birth rate, $b$ is the per capita death rate, $\beta_j$ is the transmission rate of strain $j$, $\nu_j$ the rate of recovery of individuals infected with strain $j$, and $\alpha_j$ the rate of death of individuals infected with strain $j$.


[^1]: Bremermann HJ, Thieme HR. A competitive exclusion principle for pathogen virulence. J Math Biol. 1989;27(2):179-90. doi: 10.1007/BF00276102. PMID: 2723551.
