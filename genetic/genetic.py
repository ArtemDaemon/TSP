from random import randint, shuffle
from progress.bar import ChargingBar as Bar

from .gene import Gene

ITERATIONS = 1000
POPULATION_SIZE = 100
MUTATION_ATTEMPT_LIMIT = 100


def create_route(length, first_step):
    """
    Creating a route by shuffling a list of points with an excluded starting point
    :param length: Number of cities
    :param first_step: Start city index
    :return: Generated route
    """
    route = list(range(length))
    route.remove(first_step)
    shuffle(route)
    route.insert(0, first_step)
    route.append(first_step)
    return route


def calculate_distance(route, matrix, length):
    """
    Method for calculating route distance
    :param route: List of consecutively visited cities
    :param matrix: Distance matrix between cities
    :param length: Number of cities
    :return: Route length
    """
    distance = 0
    i = 0
    while i < length:
        distance += matrix[route[i]][route[i + 1]]
        i += 1
    return distance


def mutate(route, length):
    """
    Method for route mutation. Two random elements of the route are taken (but not the first or last) and swapped
    :param route: List of consecutively visited cities
    :param length: Number of cities
    :return: Mutated Route
    """
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
    """
    Method for generating the first generation
    :param matrix: Distance matrix between cities
    :param length: Number of cities
    :param first_step: Start city index
    :return: List of first generation routes
    """
    first_generation = []
    for i in range(POPULATION_SIZE):
        new_route = create_route(length, first_step)
        first_generation.append(Gene(new_route, calculate_distance(new_route, matrix, length)))
    return first_generation


def solve_tsp(matrix, length, first_step):
    """
    main method. First, the first generation is generated.
    After that, each one mutates in turn until a more efficient one is found for each route.
    Among each generation is the most effective
    :param matrix: Distance matrix between cities
    :param length: Number of cities
    :param first_step: Start city index
    :return: The route with the minimum length found
    """
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

            attempt = 0
            while mutated_distance > current_distance:
                mutated_route = mutate(current_gene.get_route(), length)
                mutated_distance = calculate_distance(mutated_route, matrix, length)

                attempt += 1
                if attempt == MUTATION_ATTEMPT_LIMIT:
                    mutated_route = current_gene.get_route()
                    mutated_distance = current_distance
                    break

            new_gene = Gene(mutated_route, mutated_distance)
            new_generation.append(new_gene)

            if mutated_distance < min_distance:
                min_distance = mutated_distance
                final_route = mutated_route

        generation = new_generation
        bar.next()
    bar.finish()
    return min_distance, final_route
