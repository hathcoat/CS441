# Cody Hathcoat     CS441       Aug 4th

import random
import matplotlib.pyplot as plt

BOARD_SIZE = 8

#Create a random individual representation of an 8-queen board
def generate_individual():
    return [random.randint(0, BOARD_SIZE - 1) for _ in range(BOARD_SIZE)] 

#Create a list of random individuals
def generate_population(size):
    return [generate_individual() for _ in range(size)]

#Find the fitness as the number of non attacking queen pairs (max 28)
def compute_fitness(individual):
    attacking = 0

    #Loop through each piece 
    for i in range(len(individual)):
        #Check all next pieces
        for j in range(i + 1, len(individual)):
            #Check for row, column, and diagonol attack
            if individual[i] == individual[j] or abs(individual[i]-individual[j]) == abs(i-j):
                attacking += 1

    return 28 - attacking #Return fitness number

#Use roulette wheel selection to chose individuals
def select_parents(population, fitnesses):
    total_fitness = sum(fitnesses)
    #Fail safe, pick random parents if everyone is terrible
    if total_fitness == 0:
        return random.sample(population, 2)
    
    selection_probs = [f /total_fitness for f in fitnesses]
    parents = random.choices(population, weights=selection_probs, k=2)
    return parents[0], parents[1]

#Single point crossover between two parents
def crossover(parent1, parent2):
    point = random.randint(1, BOARD_SIZE - 2) #Avoid trivial crossover.
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

#Randomly mutate one gene of the individual with a given probability
def mutate(individual, mutation_rate):
    if random.random() < mutation_rate:
        index = random.randint(0, BOARD_SIZE-1)
        new_value = random.randint(0, BOARD_SIZE-1)
        individual[index] = new_value

#Run the Genetic Algorithm
def run_ga(pop_size=100, mutation_rate = 0.03, generations=2000):
    population = generate_population(pop_size)
    avg_fitness_history = []
    best_fitness_history = []

    initial_sample = population[0]
    mid_sample = None
    completed_generations = 0
    mid_recorded = False

    #Loop through the generations
    for generation in range(generations):
        fitnesses = [compute_fitness(ind) for ind in population]
        next_gen = []

        best_fitness = max(fitnesses)
        avg_fitness = sum(fitnesses) / len(fitnesses)

        best_fitness_history.append(best_fitness)
        avg_fitness_history.append(avg_fitness)

        completed_generations += 1

        print(f"Generation {generation}: Best = {best_fitness}, Avg = {avg_fitness:.2f}")

        #Handle middle for displaying
        if not mid_recorded and generation >= generations // 2:
            mid_sample = population[0]
            mid_recorded = True

        #Handle children
        while len(next_gen) < pop_size:
            p1, p2 = select_parents(population, fitnesses)
            c1, c2 = crossover(p1, p2)
            mutate(c1, mutation_rate)
            mutate(c2, mutation_rate)
            next_gen.extend([c1, c2])

        population = next_gen[:pop_size] #Trim extra children if needed

    #Safety net: if optimal solution was found before midpoint
    if mid_sample is None and len(avg_fitness_history) > 0:
        mid_index = len(avg_fitness_history) // 2
        mid_sample = population[0]

    return population, avg_fitness_history, best_fitness_history, initial_sample, mid_sample

#Print the board for report
def print_board(individual):
    for row in range(BOARD_SIZE):
        line = ""
        for col in range(BOARD_SIZE):
            line += "Q" if individual[col] == row else ". "
        print(line)
    print()

#Plot the average and best fitness
def plot_fitness(avg_fitness, best_fitness):
    generations = list(range(len(avg_fitness)))
    plt.plot(generations, avg_fitness, label="Average Fitness")
    plt.plot(generations, best_fitness, label="Best Fitness")
    plt.xlabel("Generations")
    plt.ylabel("Fitness")
    plt.title("Fitness Over Generations")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    POPULATION_SIZE = 100
    MUTATION_RATE = 0.03
    GENERATIONS = 2000

    final_population, avg_fitness, best_fitness, initial_sample, mid_sample = run_ga(
        pop_size=POPULATION_SIZE,
        mutation_rate=MUTATION_RATE,
        generations=GENERATIONS
    )

    final_fitnesses = [compute_fitness(ind) for ind in final_population]
    best_index = final_fitnesses.index(max(final_fitnesses))
    best_solution = final_population[best_index]

    print("\n=== Example Boards from Key Generations ===")
    print("Initial (Gen 0), Fitness =", compute_fitness(initial_sample))
    print_board(initial_sample)

    if mid_sample is not None:
        print("Midpoint Generation, Fitness =", compute_fitness(mid_sample))
        print_board(mid_sample)
    else:
        print("Midpoint sample not captured.")

    print("Final Best, Fitness =", final_fitnesses[best_index])
    print_board(best_solution)

    plot_fitness(avg_fitness, best_fitness)

if __name__ == "__main__":
    main()