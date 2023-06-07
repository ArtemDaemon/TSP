import io
import math
import csv
from progress.bar import ChargingBar as Bar

from genetic import genetic

START_POINT = 3753
MAX_VALUE = 17976931348623157.0


def create_matrix(data):
    """
    Method for generating a matrix from a set of point coordinates.
    Calculation of the distance between points using the Euclidean metric.
    :param data: List of coordinates
    :return: Distance matrix between cities
    """
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
    """
    Method for converting route data to the form: [iteration number], [distance from previous point to next]
    :param route: List of route points
    :param matrix: Distance matrix between cities
    :return: Formatted route data
    """
    result = []
    i = 0
    while i < (len(route) - 1):
        result.append([i, matrix[route[i]][route[i + 1]]])
        i += 1
    return result


def read_csv(filename):
    """
    Method for reading a CSV file. Only the last two columns of each row are taken into account, except for the header
    :param filename: The name of the file with the format
    :return: Array of lines from a file
    """
    result = []
    with io.open(filename, mode='r', encoding='utf-8', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(spamreader)
        for row in spamreader:
            result.append([int(x) for x in row[-2:]])
    return result


def write_csv(filename, data):
    """
    Method for writing data to CSV file
    :param filename: The name of the file with the format
    :param data: Formatted route data
    """
    with open(filename, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['Id', 'Predicted'])
        for row in data:
            spamwriter.writerow(row)


def main():
    print('Reading CSV-file')
    data = read_csv('data.csv')

    print('Creating the matrix')
    matrix = create_matrix(data)

    print('Start Solving')
    distance, route = genetic.solve_tsp(matrix, len(matrix), START_POINT)

    print('Formatting the output')
    formatted_route = format_route(route, matrix)

    print('Writing CSV-file')
    write_csv('solution.csv', formatted_route)

    print('Done!')


if __name__ == '__main__':
    main()
