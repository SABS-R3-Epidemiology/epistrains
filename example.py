from epistrains import Population, make_br, Strain, Solver

# Generate an exponential birth rate function: N*a*exp(-k*N)
birth_rate_function = make_br(a=1.0, k=0.001)

# Instantiate the population class with a death rate = 0.00005, and initial population size = 10,000
# and the exponential birth rate function defined above.
population = Population(death=0.00005, size=10000, birth_function=birth_rate_function)

# Generate two strains to model.
# Strain I1 has a death rate, alpha=0.0, recovery rate, nu=0.05, and a transmission rate, beta=0.005.
# At the start of the simulation 3 individuals are infected with strain I1.
# Strain I2 has a death rate, alpha=0.005, recovery rate, nu=0.04, and a transmission rate, beta=0.007.
# At the start of the simulation 8 individuals are infected with strain I2.
I1 = Strain(alpha=0.0, nu=0.05, beta=0.005, infected=3)
I2 = Strain(alpha=0.005, nu=0.04, beta=0.007, infected=8)

# Instantiate the Solver class, providing it with the population structure and the two strains to be modelled.
model = Solver(pop=population, strains=[I1, I2], time=1)

# Solve the set of equations for the 4 compartments.
model.solve()

# Plot the results to be displayed, and not saved.
model.plot_compartments()
# model.save_compartments('epistrains_example.png')
