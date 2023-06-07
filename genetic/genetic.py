from random import randint

from Gene import Gene

ITERATIONS = 5
POPULATION_SIZE = 10
DIVIDER_RATE = 2000


def create_route(length, first_step):
    route = [first_step]
    while len(route) < length:
        new_step = randint(0, length - 1)
        if new_step not in route:
            route.append(new_step)
    route.append(first_step)
    return route


def calculate_distance(route, matrix, length):
    distance = 0
    i = 0
    while i < length:
        distance += matrix[route[i]][route[i + 1]]
        i += 1
    return distance


def solve_tsp(matrix, length, first_step):
    population = []

    for i in range(POPULATION_SIZE):
        new_route = create_route(length, first_step)
        population.append(Gene(new_route, calculate_distance(new_route, matrix, length)))

    min_distance = population[0].get_distance()
    final_route = population[0].get_route()

    while
