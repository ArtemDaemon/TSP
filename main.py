import math
import numpy as np
import csv

from Node import Node


def solve_tsp(matrix):
    nodes = []

    line_indexes, column_indexes = create_indexes_lists(matrix)
    start_node = Node(matrix.copy(), 0, [], line_indexes, column_indexes)

    nodes.append(start_node)
    current_node = pop_min_node(nodes)

    while current_node.get_length() > 2:
        new_nodes = current_node.subset()
        for new_node in new_nodes:
            nodes.append(new_node)
        current_node = pop_min_node(nodes)

    current_node.parse()
    return current_node.h, current_node.steps


def pop_min_node(nodes):
    min_node = nodes[0]
    index = 0
    for i, node in enumerate(nodes):
        if node.get_h() < min_node.get_h():
            min_node = node
            index = i
    del nodes[index]
    return min_node


def create_indexes_lists(matrix):
    indexes_list = list(range(0, len(matrix)))
    return indexes_list, indexes_list.copy()


def create_matrix(data):
    matrix = []
    for i, point_x in enumerate(data):
        line = []
        for j, point_y in enumerate(data):
            if i == j:
                euclidian_distance = -1
            else:
                euclidian_distance = math.sqrt((point_x[0] - point_y[0]) ** 2 + (point_x[1] - point_y[1]) ** 2)
            line.append(euclidian_distance)
        matrix.append(line)
    return np.array(matrix)


def format_steps(steps, first_point, matrix):
    result = []
    temp_steps = steps.copy()
    for i in range(0, len(steps) - 1):
        for j, step in enumerate(temp_steps):
            if step[0] == first_point:
                distance = matrix[step[0]][step[1]]
                result.append([i, distance])
                first_point = step[1]
                del temp_steps[j]
                break
    return result


def read_csv(filename):
    result = []
    with open(filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(spamreader)
        for row in spamreader:
            result.append([int(x) for x in row[-2:]])
    return result


def write_csv(filename, data):
    with open(filename, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in data:
            spamwriter.writerow(row)


if __name__ == '__main__':
    data = read_csv('data_top5.csv')
    matrix = create_matrix(data)
    #
    # matrix = np.array([[-1, 20, 18, 12, 8],
    #                    [5, -1, 14, 7, 11],
    #                    [12, 18, -1, 6, 11],
    #                    [11, 17, 11, -1, 12],
    #                    [5, 5, 5, 5, -1]])
    distance, steps = solve_tsp(matrix)
    formatted_steps = format_steps(steps, 0, matrix)
    write_csv('solution.csv', formatted_steps)
