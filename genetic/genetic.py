from random import randint, shuffle
from progress.bar import ChargingBar as Bar

from .gene import Gene

ITERATIONS = 100000
POPULATION_SIZE = 100
DIVIDER = 10000
DEVIATION_EXP = 100
DEVIATION_THRESHOLD = 0.5
MUTATION_ATTEMPT_LIMIT = 100


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


def create_first_generation(matrix, length, first_step):
    first_generation = []
    for i in range(POPULATION_SIZE):
        new_route = create_route(length, first_step)
        first_generation.append(Gene(new_route, calculate_distance(new_route, matrix, length)))
    return first_generation


def solve_tsp(matrix, length, first_step):
    generation = create_first_generation(matrix, length, first_step)

    min_distance = generation[0].get_distance()
    final_route = generation[0].get_route()

    bar = Bar('Processing', max=ITERATIONS, suffix='%(percent)d%% [%(index)d/%(max)d]')

    for i in range(ITERATIONS):
        new_generation = []
        for j in range(POPULATION_SIZE):
            current_gene = generation[j]
            current_distance = current_gene.get_distance()

            mutated_route = current_gene.get_route()
            mutated_distance = current_distance + 1
            deviation = False

            attempt = 0
            while mutated_distance <= current_distance and not deviation and attempt < MUTATION_ATTEMPT_LIMIT:
                mutated_route = mutate(current_gene.get_route(), length)
                mutated_distance = calculate_distance(mutated_route, matrix, length)

                deviation_factor = pow(DEVIATION_EXP, -1 * (mutated_distance - current_gene.get_distance()) / DIVIDER)
                if deviation_factor > DEVIATION_THRESHOLD:
                    deviation = True
                attempt += 1

            new_gene = Gene(mutated_route, mutated_distance)
            new_generation.append(new_gene)

            if mutated_distance < min_distance:
                min_distance = mutated_distance
                final_route = mutated_route

        generation = new_generation
        bar.next()
    bar.finish()
    return min_distance, final_route
