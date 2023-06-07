import io
import math
import csv
from progress.bar import ChargingBar as Bar

from genetic import genetic

START_POINT = 3753
MAX_VALUE = 17976931348623157.0


def create_matrix(data):
    bar = Bar('Creating', max=len(data), suffix='%(percent)d%% [%(index)d/%(max)d]')
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
        bar.next()
    bar.finish()
    return matrix


def format_route(route, matrix):
    result = []
    i = 0
    print(len)
    while i < len(route):
        print(i)
        result.append([i, matrix[route[i]][route[i + 1]]])
        i += 1
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
    print('Reading CSV-file')
    data = read_csv('data.csv')

    print('Creating the matrix')
    matrix = create_matrix(data)

    print('Start Solving')
    distance, route = genetic.solve_tsp(matrix, len(matrix), START_POINT)
    formatted_route = format_route(route, matrix)
    print(route[0])
    print(route[1])
    print('/////////////')
    print(formatted_route[0])


if __name__ == '__main__':
    main()
