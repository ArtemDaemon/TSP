import numpy as np


class Node(object):
    def __init__(self, matrix, h, steps, line_indexes, column_indexes):
        self.matrix, self.h = self.reduction(matrix)
        self.h += h

        self.steps = steps
        self.line_indexes = line_indexes
        self.column_indexes = column_indexes

    def get_h(self):
        return self.h

    def add_step(self, branch):
        self.steps.append(branch)

    # REDUCTION
    @staticmethod
    def reduction(matrix):
        matrix, h1 = Node.reduction_lines(matrix)
        matrix, h2 = Node.reduction_columns(matrix)
        return matrix, h1 + h2

    @staticmethod
    def reduction_lines(matrix):
        h = 0
        for line in matrix:
            d = line[0]
            for value in line:
                if value == -1:
                    continue
                if d == -1 or value < d:
                    d = value
            for i, value in enumerate(line):
                if value == -1:
                    continue
                line[i] -= d
            h += d
        return matrix, h

    @staticmethod
    def reduction_columns(matrix):
        h = 0
        for i, line in enumerate(matrix.T):
            d = line[0]
            for value in line:
                if value == -1:
                    continue
                if d == -1 or value < d:
                    d = value
            for j, value in enumerate(line):
                if value == -1:
                    continue
                matrix[j][i] -= d
            h += d
        return matrix, h

    # END REDUCTION
    # SUBSET
    def subset(self):
        branch = self.define_branch(self.matrix)
        excluded_node = self.exclude_branch(branch)
        included_node = self.include_branch(branch)
        return [excluded_node, included_node]

    # DEFINING BRANCH
    @staticmethod
    def define_branch(matrix):
        zero_indexes = Node.find_zeros(matrix)
        mins = Node.find_mins(matrix, zero_indexes)
        max_min = Node.find_max_min(mins)
        return zero_indexes[mins.index(max_min)]

    @staticmethod
    def find_zeros(matrix):
        zero_indexes = []
        for i, line in enumerate(matrix):
            for j, column in enumerate(line):
                if column == 0:
                    zero_indexes.append([i, j])
        return zero_indexes

    @staticmethod
    def find_mins(matrix, zero_indexes):
        min_in_lines = Node.find_min_in_lines(matrix, zero_indexes)
        min_in_columns = Node.find_min_in_columns(matrix, zero_indexes)
        return [x + y for x, y in zip(min_in_lines, min_in_columns)]

    @staticmethod
    def find_min_in_lines(matrix, zero_indexes):
        min_in_lines = []
        for zero_index in zero_indexes:
            line = matrix[zero_index[0]]
            min_value = -1
            for i, value in enumerate(line):
                if value == -1 or i == zero_index[1]:
                    continue
                if min_value == -1 or value < min_value:
                    min_value = value
            min_in_lines.append(min_value)
        return min_in_lines

    @staticmethod
    def find_min_in_columns(matrix, zero_indexes):
        min_in_columns = []
        for zero_index in zero_indexes:
            column = matrix.T[zero_index[1]]
            min_value = -1
            for i, value in enumerate(column):
                if value == -1 or i == zero_index[0]:
                    continue
                if min_value == -1 or value < min_value:
                    min_value = value
            min_in_columns.append(min_value)
        return min_in_columns

    @staticmethod
    def find_max_min(mins):
        result = mins[0]
        for min in mins:
            if min > result:
                result = min
        return result

    # END OF DEFINING BRANCH

    def exclude_branch(self, branch):
        new_matrix = self.matrix.copy()
        new_matrix[branch[0]][branch[1]] = -1
        return Node(new_matrix, self.h, self.steps.copy(), self.line_indexes.copy(), self.column_indexes.copy())

    def include_branch(self, branch):
        new_matrix = self.matrix.copy()

        branch_line = self.line_indexes[branch[0]]
        branch_column = self.column_indexes[branch[1]]
        excluded_line = self.indexes_lists[0].index(branch_column)
        excluded_column = self.indexes_lists[1].index(branch_line)

        new_matrix[excluded_line][excluded_column] = -1
        new_matrix = np.delete(new_matrix, branch[0], axis=0)
        new_matrix = np.delete(new_matrix, branch[1], axis=1)

        new_steps = self.steps.copy()
        new_steps.append([branch_line, branch_column])

        new_indexes_lists = self.indexes_lists.copy()
        del new_indexes_lists[0][branch[0]]
        del new_indexes_lists[1][branch[1]]
        print(self.indexes_lists)

        return Node(new_matrix, self.h, new_steps, new_indexes_lists)

    # END SUBSET

    def display(self):
        print(self.indexes_lists)
        print(self.matrix)
        print(self.h)
        print(self.steps)
