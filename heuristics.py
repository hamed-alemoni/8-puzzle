from math import sqrt
from Cell import Cell
# calculates heuristic value of a cell(Euclidean distance)
def first_heuristic(destination_row, destination_column, cell ):

    return distance_between_two_coordinates((destination_row, destination_column), (cell.row, cell.column))


# calculates heuristic value of a cell(Manhattan distance)
def second_heuristic(destination_row, destination_column, cell):

    distance_from_left = distance_between_two_coordinates((cell.row, cell.column), (cell.row, destination_column))

    distance_from_up = distance_between_two_coordinates((destination_row, destination_column), (cell.row, destination_column))

    result = distance_from_up + distance_from_left

    return result

# bonus heuristic(Diagonal distance)
def third_heuristic(destination_row, destination_column, cell):
    
    length_of_nodes = 1

    diagonal_distance_between_each_node = sqrt(2)

    x_distance = abs(cell.row - destination_row)

    y_distance = abs(cell.column - destination_column)

    result = length_of_nodes * (x_distance + y_distance) + (diagonal_distance_between_each_node - 2 * length_of_nodes) * min(x_distance, y_distance)

    return result




def distance_between_two_coordinates(first, second):
    x = (first[0] - second[0]) ** 2
    y = (first[1] - second[1]) ** 2
    result = sqrt(x + y)
    return result

