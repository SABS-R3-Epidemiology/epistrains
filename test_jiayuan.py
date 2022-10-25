from epistrains import Population, make_br, Strain, Solver

birth_rate_function = make_br(a=1.2, k=0.03)

population = Population(death=0.005, size=1000, birth_function=birth_rate_function)

I1 = Strain(alpha=0.000001, nu=0.5, beta=0.9, infected=3)
I2 = Strain(alpha=0.000001, nu=0.5, beta=0.9, infected=3)

model = Solver(pop=population, strains=[I1, I2], time=1)
solution = model.solve()
print(solution.y.T)

#Solver.plot_compartments(solution)