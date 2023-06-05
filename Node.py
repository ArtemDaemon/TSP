class Node(object):
    def __init__(self, matrix, h):
        self.matrix, self.h = self.reduction(matrix, h)
        self.steps = []

    def get_h(self):
        return self.h

    def add_step(self, branch):
        self.steps.append(branch)

    # REDUCTION
    @staticmethod
    def reduction(matrix, h):
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
        excluded_node = self.exclude_branch(self, branch)
        included_node = self.include_branch(self, branch)
        if h1 < h2:
            matrix = matrix1
            h = h1
            step = None
        else:
            matrix = matrix2
            h = h2
            step = branch
        return matrix, h, step

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

    def exclude_branch(matrix, branch):
        new_matrix = matrix[branch[0]][branch[1]]
        excluded_node = Node(matrix.copy())
         = -1
        node_matrix, h = reduction(matrix)
        return Node(node_matrix, h)


    def include_branch(matrix, branch):
        matrix[branch[1]][branch[0]] = -1
        matrix = np.delete(matrix, branch[0], axis=0)
        matrix = np.delete(matrix, branch[1], axis=1)
        node_matrix, h = reduction(matrix)
        return Node(node_matrix, h)

    # END SUBSET

    def display(self):
        print(self.matrix)
        print(self.h)
        print(self.steps)
