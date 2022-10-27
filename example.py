from epistrains import Population, make_br, Strain, Solver

# Generate an exponential birth rate function: N*a*exp(-k*N)
birth_rate_function = make_br(a=10.0, k=0.001)

# Instantiate the population class with a death rate = 0.0, and initial population size = 150,000
# and the exponential birth rate function defined above.
population = Population(death=0.0, size=150000, birth_function=birth_rate_function)

# Generate two strains to model.
# Strain I1 has a death rate, alpha=0.0, recovery rate, nu=0.143, and a transmission rate, beta=0.000003.
# At the start of the simulation 150 individuals are infected with strain I1.
# Strain I2 has a death rate, alpha=0.002, recovery rate, nu=0.2, and a transmission rate, beta=0.00000429.
# At the start of the simulation 10 individuals are infected with strain I2.
I1 = Strain(alpha=0.0, nu=0.143, beta=0.000003, infected=150)
I2 = Strain(alpha=0.002, nu=0.2, beta=0.00000429, infected=10)

# Instantiate the Solver class, providing it with the population structure and the two strains to be modelled,
# as well as the total time over which to run the simulation.
model = Solver(pop=population, strains=[I1, I2], time=70)

# Solve the set of equations for the 4 compartments.
model.solve()

# Plot the results to be displayed, and not saved.
model.plot_compartments()
