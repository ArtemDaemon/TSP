from random import randint

# from Gene import Gene

ITERATIONS = 5
POPULATION_SIZE = 10


def create_route(length, first_step):
    route = [first_step]
    while len(route) < length:
        new_step = randint(0, length - 1)
        if chr(new_step + 48) not in route:
            route.append(chr(new_step + 48))
    route.append(first_step)
    return route


def calculate_distance(route, matrix):
    pass


def solve_tsp(matrix, length, first_step):
    current_gene = 0

    for i in range(POPULATION_SIZE):
        new_route = create_route(length, first_step)
        print(new_route)
        break
        # new_gene = Gene(new_route, calculate_distance(new_route, matrix))
