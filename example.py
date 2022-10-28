from epistrains import Population, make_br, Strain, Solver

# Generate an exponential birth rate function: N*a*exp(-k*N)
birth_rate_function = make_br(a=10.0, k=0.001)

# Instantiate the population class with a death rate = 0.000006, and initial population size = 150,000
# and the exponential birth rate function defined above.
population = Population(death=0.000006, size=150000, birth_function=birth_rate_function)

# Generate two strains to model.
# Strain I1 has a case fatality rate (CFR) = 0.00007, recovery time = 7 days, and an R0 = 3.14.
# At the start of the simulation 150 individuals are infected with strain I1.
# Strain I2 has a case fatality rate (CFR) = 0.001, recovery time = 8 days, and an R0 = 4.22.
# At the start of the simulation 10 individuals are infected with strain I2.
I1 = Strain(CFR=0.00007, recovery_time=7, R0=3.14, infected=150)
I2 = Strain(CFR=0.001, recovery_time=8, R0=4.22, infected=10)

# Instantiate the Solver class, providing it with the population structure and the two strains to be modelled,
# as well as the total time over which to run the simulation.
model = Solver(pop=population, strains=[I1, I2], time=70)

# Solve the set of equations for the 4 compartments.
model.solve()

# Plot the results to be displayed, and not saved.
# model.plot_compartments()
# model.plot_death()
model.save_compartments('epistrains_example.png')
model.save_death('epistrains_death_example.png')
