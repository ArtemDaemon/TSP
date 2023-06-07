from progress.bar import ChargingBar as Bar

from Node import Node


async def solve_tsp(matrix):
    nodes = []

    line_indexes, column_indexes = create_indexes_lists(matrix)
    start_node = Node(matrix.copy(), 0, [], line_indexes, column_indexes)

    total_length = start_node.get_length()
    bar = Bar('Processing', max=total_length, suffix='%(percent)d%% [%(index)d/%(max)d]')

    nodes.append(start_node)
    current_node = pop_min_node(nodes)

    while current_node.get_length() > 2:
        new_nodes = await current_node.subset()
        # new_nodes = current_node.subset()
        for new_node in new_nodes:
            nodes.append(new_node)
        current_node = pop_min_node(nodes)
        bar.goto(total_length - current_node.get_length())
    bar.goto(total_length)
    bar.finish()
    current_node.parse()
    return current_node.h, current_node.steps


def create_indexes_lists(matrix):
    indexes_list = list(range(0, len(matrix)))
    return indexes_list, indexes_list.copy()


def pop_min_node(nodes):
    min_node = nodes[0]
    index = 0
    for i, node in enumerate(nodes):
        if node.get_h() < min_node.get_h():
            min_node = node
            index = i
    del nodes[index]
    return min_node
