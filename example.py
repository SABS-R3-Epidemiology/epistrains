from epistrains import Population, make_br, Strain, Solver, plot_compartments

birth_rate_function = make_br(a=100.0, k=3.0)

population = Population(death=0.05, size=1000, birth_function=birth_rate_function)

I1 = Strain(alpha=0.1, nu=0.1, beta=0.1, infected=5)
I2 = Strain(alpha=0.1, nu=0.3, beta=0.1, infected=3)

model = Solver(pop=population, strains=[I1, I2], time=10)
solution = model.solve()

plot_compartments(solution)
