import io
import math
import csv

from genetic import genetic

# START_POINT = 3753
START_POINT = 0
MAX_VALUE = 17976931348623157.0


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
    return matrix


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
    with io.open(filename, mode='r', encoding='utf-8', newline='') as csvfile:
        # with open(filename, newline='') as csvfile:
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


def main():
    # print('Reading CSV-file')
    # data = read_csv('data.csv')
    #
    # print('Creating the matrix')
    # matrix = create_matrix(data)
    matrix = [[MAX_VALUE, 20, 18, 12, 8],
              [5, MAX_VALUE, 14, 7, 11],
              [12, 18, MAX_VALUE, 6, 11],
              [11, 17, 11, MAX_VALUE, 12],
              [5, 5, 5, 5, MAX_VALUE]]

    print('Start Solving')
    distance, route = genetic.solve_tsp(matrix, len(matrix), START_POINT)
    print(distance)
    print(route)


if __name__ == '__main__':
    main()
