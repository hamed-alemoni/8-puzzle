from Cell import make_cells, Cell, is_puzzle_solved, determine_action, move, find_depth, save_and_move_action
import copy

# global_variables

cells = make_cells()
final_cells = None
# count number of expanded nodes
nodes_counter = 0
# save actions
actions = ''
# save visited node
visited = set()
def iterative_deepending_search(start_cell, goal_cell, max_limit):
    global nodes_counter,actions, visited, final_cells
    parent = None

    for limit in range(max_limit):
        nodes_counter = 0
        actions = ''
        final_cells = copy.deepcopy(cells)
        cost = depth_limited_search(parent, start_cell, goal_cell, limit)
        visited.clear()
        if cost != -1:
            return cells[0][0].distance_from_start_cell
    return -1
# create children of start_state in specific depth
def depth_limited_search(parent, start_state, goal, limit):
    global nodes_counter, actions, visited

    if limit < 0:
        return -1

    set_g(parent, start_state)

    parent, action = save_and_move_action(parent, start_state, final_cells)
    actions += action


    if start_state.is_destination(goal):
        return start_state.distance_from_start_cell
    
    nodes_counter += 1

    visited.add(start_state.value)
    
    for child in children(start_state):
        if child is not None and child.value not in visited:

            if depth_limited_search(parent, child, goal, limit - 1) != -1:
                return child.distance_from_start_cell

    
    return -1

# set distance from start cell for child cell
def set_g(parent, child):
    global visited
    if child not in visited:
        if parent is not None:
            child.distance_from_start_cell = parent.distance_from_start_cell + 1
        else:
            child.distance_from_start_cell = 0

def children(parent, cells=cells):
    children = []

    children.append(create_left_children(parent, cells))
    children.append(create_up_children(parent, cells))
    children.append(create_right_children(parent, cells))
    children.append(create_down_children(parent, cells))
    
    return children

def create_left_children(parent, cells=cells):
    left = None
    if parent.is_unblocked_left():
        # create left child
        left = cells[parent.row][parent.column - 1]
        parent.left = left
        # set_g(parent, left)


    return left

def create_right_children(parent, cells=cells):
    right = None
    if parent.is_unblocked_right():
        # create right child
        right = cells[parent.row][parent.column + 1]
        parent.right = right
        # set_g(parent, right)

    return right

def create_up_children(parent, cells=cells):
    up = None
    if parent.is_unblocked_up():
        # create up child
        up = cells[parent.row - 1][parent.column]
        parent.up = up
        # set_g(parent, up)

    return up

def create_down_children(parent, cells=cells):
    down = None
    if parent.is_unblocked_down():
        # create down child
        down = cells[parent.row + 1][parent.column]
        parent.down = down
        # set_g(parent, down)

    return down

def main (input_text):
    global nodes_counter, actions
    puzzle = str(input_text).split()
    initialize_cells(puzzle)

    for i in range(Cell.MAX_ROW):
        for j in range(Cell.MAX_COLUMN):
            current_cell = cells[i][j]
            current_cell.distance_from_start_cell = 0
            if current_cell.value == 0:
                total_cost = iterative_deepending_search(current_cell, Cell(0,0),4)
    is_solved = is_puzzle_solved(final_cells)
    depth = find_depth(cells)
    result = (total_cost, nodes_counter, actions, is_solved,cells,final_cells, depth)
    nodes_counter = 0
    actions = ''
    
    return result


def initialize_cells(puzzle):
    global cells
    row = 0
    for i in range(len(puzzle)):
        if i >= 3 and i % 3 == 0:
            row += 1
        column = i % 3
        cell = Cell(row,column,int(puzzle[i]))
        cells[row][column] = cell
