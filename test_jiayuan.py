from epistrains import Population, make_br, Strain, Solver

birth_rate_function = make_br(a=1.0, k=0.001)
population = Population(death=0.00005, size=10000, birth_function=birth_rate_function)

I1 = Strain(alpha=0.0, nu=0.05, beta=0.005, infected=3)
I2 = Strain(alpha=0.005, nu=0.04, beta=0.007, infected=8)

model = Solver(pop=population, strains=[I1, I2], time=1)
solution = model.solve()

# print(solution.y.T)

Solver.plot_compartments(solution)
