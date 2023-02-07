from Cell import Cell, make_cells, move, determine_action, is_puzzle_solved, find_depth, save_and_move_action
import copy

# global_variables

cells = make_cells()
final_cells = None
# count number of expanded nodes
nodes_counter = 0
# save actions
actions = ''

def uniform_cost_search(start_cell, goal_cell):
    global nodes_counter, actions
    fringe = []
    visited = dict()
    parent = None
    fringe.append(start_cell)
    while len(fringe) != 0:
        minimum_g_cost_cell = find_minimum_g(fringe, visited)

        parent, action = save_and_move_action(parent, minimum_g_cost_cell, final_cells)
        actions += action

        nodes_counter += 1

        visited[minimum_g_cost_cell.value] = True

        fringe.pop(fringe.index(minimum_g_cost_cell))

        if minimum_g_cost_cell.is_destination(goal_cell):
            return minimum_g_cost_cell.distance_from_start_cell
        
        right_child_condition(minimum_g_cost_cell, fringe, visited)
        left_child_condition(minimum_g_cost_cell, fringe, visited)
        down_child_condition(minimum_g_cost_cell, fringe, visited)
        up_child_condition(minimum_g_cost_cell, fringe, visited)

def find_minimum_g(fringe, visited):
    minimum_cell = None
    min_g = 999999999

    if len(fringe) == 1:
        return fringe[0]

    for cell in fringe:
        if min_g >= cell.distance_from_start_cell and cell.value not in visited.keys():
            min_g = cell.distance_from_start_cell
            minimum_cell = cell
    
    return minimum_cell


#####################################  RIGHT CHILD CONDITIONS #####################################

# calculate distance from start cell (g) when the right child row and column is valid and the right child hasn't visisted
def right_child_condition(parent, fringe, visited):
    if parent.is_unblocked_right():
        # right child is existed
        right_child = cells[parent.row][parent.column + 1]

        if right_child.value not in visited.keys():
            right_child.distance_from_start_cell = parent.distance_from_start_cell + 1
            fringe.append(right_child)
            parent.right = right_child


#####################################  UP CHILD CONDITIONS #####################################

# calculate distance from start cell (g) when the up child row and column is valid and the right child hasn't visisted
def up_child_condition(parent, fringe, visited):
    if parent.is_unblocked_up():
        # up child is existed
        up_child = cells[parent.row - 1][parent.column]

        if up_child.value not in visited.keys():
            up_child.distance_from_start_cell = parent.distance_from_start_cell + 1
            fringe.append(up_child)
            parent.up = up_child

#####################################  LEFT CHILD CONDITIONS #####################################

# calculate distance from start cell (g) when the left child row and column is valid and the right child hasn't visisted
def left_child_condition(parent, fringe, visited):
    if parent.is_unblocked_left():
        # left chid is existed
        left_child = cells[parent.row][parent.column - 1]

        if left_child.value not in visited.keys():
            left_child.distance_from_start_cell = parent.distance_from_start_cell + 1
            fringe.append(left_child)
            parent.left = left_child

#####################################  DOWN CHILD CONDITIONS #####################################

# calculate distance from start cell (g) when the left child row and column is valid and the right child hasn't visisted
def down_child_condition(parent, fringe, visited):
    if parent.is_unblocked_down():
        # down child is existed
        down_child = cells[parent.row + 1][parent.column]

        if down_child.value not in visited.keys():
            down_child.distance_from_start_cell = parent.distance_from_start_cell + 1
            fringe.append(down_child)
            parent.down = down_child


def main (input_text):
    global nodes_counter, actions
    puzzle = str(input_text).split()

    initialize_cells(puzzle)

    for i in range(Cell.MAX_ROW):
        for j in range(Cell.MAX_COLUMN):
            current_cell = cells[i][j]
            current_cell.distance_from_start_cell = 0
            if current_cell.value == 0:
                total_cost = uniform_cost_search(current_cell, Cell(0,0))
    is_solved = is_puzzle_solved(final_cells)
    depth = find_depth(cells)
    result = (total_cost, nodes_counter, actions, is_solved,cells,final_cells, depth)
    nodes_counter = 0
    actions = ''
    return(result)


def initialize_cells(puzzle):
    global cells, final_cells
    row = 0
    for i in range(len(puzzle)):
        if i >= 3 and i % 3 == 0:
            row += 1
        column = i % 3
        cell = Cell(row,column,int(puzzle[i]))
        cells[row][column] = cell
    final_cells = copy.deepcopy(cells)

