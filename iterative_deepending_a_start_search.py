from Cell import make_cells, is_puzzle_solved, determine_action, move, Cell, find_depth, save_and_move_action
from a_star_search import calculate_f, determine_heuristic
from iterative_deepending_search import children
import sys, copy

# global_variables

cells = make_cells()
final_cells = None
# count number of expanded nodes
nodes_counter = 0
# save actions
actions = ''

def iterative_deepending_a_star_search(start_cell, goal_cell):
    global nodes_counter, actions
    set_g_h_f(start_cell, None, goal_cell)

    # initialize bound, minimum and check variables
    bound = start_cell.f
    minimum = sys.maxsize
    check = 0
    parent = None

    while check == 0:
        check = depth_limited_search(parent, start_cell, goal_cell, bound, minimum)
        bound = minimum

    return cells[0][0].distance_from_start_cell


def depth_limited_search(parent , start_state, goal, bound, minimum):
    global nodes_counter, actions

    # f is greater than bound limit  
    if start_state.f > bound:
        return -1

    parent, action = save_and_move_action(parent, start_state, final_cells)
    actions += action

    # found the goal state
    if start_state.is_destination(goal):
        return start_state.distance_from_start_cell

    nodes_counter += 1
    
    # check start_state children to find new path
    for child in children(start_state,cells):
        if child is not None:
            # set f, g and h
            set_g_h_f(child, start_state, goal)

            # find minimum f cost
            if minimum > child.f:
                minimum = child.f
            

            if depth_limited_search(parent, child, goal, bound, minimum) != -1:
                return child.distance_from_start_cell
    

    return -1


# set g, h, f for child
def set_g_h_f(child, parent, goal):

    g, h, f = calculate_f(child, parent, goal)

    child.distance_from_start_cell = g

    child.distance_from_end_cell = h

    child.f = f

def main (input_text, heuristic_type):
    global nodes_counter, actions
    puzzle = str(input_text).split()
    determine_heuristic(heuristic_type)
    initialize_cells(puzzle)

    for i in range(Cell.MAX_ROW):
        for j in range(Cell.MAX_COLUMN):
            current_cell = cells[i][j]
            current_cell.distance_from_start_cell = 0
            if current_cell.value == 0:
                total_cost = iterative_deepending_a_star_search(current_cell, Cell(0,0))
    is_solved = is_puzzle_solved(final_cells)
    depth = find_depth(cells)
    result = (total_cost, nodes_counter, actions, is_solved,cells,final_cells, depth)
    nodes_counter = 0
    actions = ''
    
    return result





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


