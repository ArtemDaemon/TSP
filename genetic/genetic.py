from random import randint, shuffle

from .gene import Gene

ITERATIONS = 100
POPULATION_SIZE = 10
DIVIDER_RATE = 2000
DEVIATION_EXP = 100
DEVIATION_THRESHOLD = 0.5


def create_route(length, first_step):
    route = list(range(length))
    route.remove(first_step)
    shuffle(route)
    route.insert(0, first_step)
    route.append(first_step)
    return route


def calculate_distance(route, matrix, length):
    distance = 0
    i = 0
    while i < length:
        distance += matrix[route[i]][route[i + 1]]
        i += 1
    return distance


def mutate(route, length):
    new_route = route.copy()
    old_index = new_index = 0
    while old_index == new_index:
        old_index = randint(1, length - 1)
        new_index = randint(1, length - 1)

    temp = new_route[old_index]
    new_route[old_index] = new_route[new_index]
    new_route[new_index] = temp

    return new_route


def solve_tsp(matrix, length, first_step):
    generation = []

    for i in range(POPULATION_SIZE):
        new_route = create_route(length, first_step)
        generation.append(Gene(new_route, calculate_distance(new_route, matrix, length)))

    min_distance = generation[0].get_distance()
    final_route = generation[0].get_route()

    for i in range(ITERATIONS):
        new_generation = []
        for j in range(POPULATION_SIZE):
            current_gene = generation[j]
            current_distance = current_gene.get_distance()

            mutated_route = current_gene.get_route()
            mutated_distance = current_distance + 1
            deviation = False

            while mutated_distance <= current_distance and not deviation:
                mutated_route = mutate(current_gene.get_route(), length)
                mutated_distance = calculate_distance(mutated_route, matrix, length)

                divider = (ITERATIONS - i) * DIVIDER_RATE
                deviation_factor = pow(DEVIATION_EXP, -1 * (mutated_distance - current_gene.get_distance()) / divider)
                if deviation_factor > DEVIATION_THRESHOLD:
                    deviation = True

            new_gene = Gene(mutated_route, mutated_distance)
            new_generation.append(new_gene)

            if mutated_distance < min_distance:
                min_distance = mutated_distance
                final_route = mutated_route

        generation = new_generation

    return min_distance, final_route


