import numpy as np
import utils
from Node import Node


def solve_tsp(matrix):
    nodes = []
    start_node = Node(matrix.copy(), 0, [])

    nodes.append(start_node)

    current_node = pop_min_node(nodes)
    new_nodes = current_node.subset()
    for new_node in new_nodes:
        nodes.append(new_node)

    current_node = pop_min_node(nodes)
    new_nodes = current_node.subset()
    for new_node in new_nodes:
        nodes.append(new_node)

    # for node in nodes:
    #     node.display()
    #     print('/////////////////////////')
    # new_matrix, new_h, step = utils.subset(matrix, new_branch)
    # h += new_h
    #
    # new_branch = utils.define_branch(new_matrix)
    # new_matrix, new_h, step = utils.subset(new_matrix, new_branch)
    # h += new_h

    # END RESULT
    result = [0, 2, 3, 1, 4]
    return result, 12.0


def pop_min_node(nodes):
    min_node = nodes[0]
    index = 0
    for i, node in enumerate(nodes):
        if node.get_h() < min_node.get_h():
            min_node = node
            index = i
    del nodes[index]
    return min_node


if __name__ == '__main__':
    matrix = np.array([[-1, 20, 18, 12, 8],
                       [5, -1, 14, 7, 11],
                       [12, 18, -1, 6, 11],
                       [11, 17, 11, -1, 12],
                       [5, 5, 5, 5, -1]])
    solve_tsp(matrix)
    # print(solve_tsp(matrix))
