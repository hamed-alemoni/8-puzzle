from heuristics import first_heuristic, second_heuristic, third_heuristic
import sys, copy
from Cell import Cell, is_puzzle_solved, make_cells, determine_action, move, find_depth, save_and_move_action

# global_variables
cells = make_cells()

final_cells = None
# count number of expanded nodes
nodes_counter = 0
# save actions
actions = ''
heuristic = None

def a_star_search(start_cell, goal_cell):
    global nodes_counter, actions
    opened_list = []
    closed_list = []
    parent = None

    opened_list.append(start_cell)

    while len(opened_list) != 0:
        

        minimum_f_cost = find_minimum_f(opened_list)

        parent, action = save_and_move_action(parent, minimum_f_cost, final_cells)
        actions += action

        
        if minimum_f_cost.is_destination(goal_cell):
            return minimum_f_cost.distance_from_start_cell

        nodes_counter += 1

        closed_list.append(minimum_f_cost)

        opened_list.pop(opened_list.index(minimum_f_cost))        

        # make minimum_f_cost's left child if it is existed
        left_child_condition(minimum_f_cost,goal_cell,closed_list,opened_list)

        # make minimum_f_cost's right child if it is existed
        right_child_condition(minimum_f_cost,goal_cell,closed_list,opened_list)

        # make minimum_f_cost's down child if it is existed
        down_child_condition(minimum_f_cost,goal_cell,closed_list,opened_list)

        # make minimum_f_cost's up child if it is existed
        up_child_condition(minimum_f_cost,goal_cell,closed_list,opened_list)


# find the cell with minimum f cost
def find_minimum_f(opened_list):

    if len(opened_list) == 1:
        return opened_list[0]

    minimum_cell = None
    min_f = 99999
    min_h = 99999
    value = 99999
    for cell in opened_list:
        if min_f > cell.f:
            min_f = cell.f
            minimum_cell = cell
            min_h = cell.distance_from_end_cell
            value = cell.value
        elif min_f == cell.f:
            if min_h > cell.distance_from_end_cell or value < cell.value :
                min_f = cell.f
                minimum_cell = cell
                min_h = cell.distance_from_end_cell
    return minimum_cell

#####################################  UP CHILD CONDITIONS #####################################
# here we check the up child is unblocked or not and it is in closed list or not
def up_child_condition(parent, goal_cell, closed_list, opened_list):
     # make minimum_f_cost's up child if it is existed
    if parent.is_unblocked_up():
        # create up child
        up = cells[parent.row - 1][parent.column]

        if up not in closed_list:
            set_and_calculate_f_up(parent, up, goal_cell)
            opened_list.append(up)
            parent.up = up


# here we set up child and set or update g, h and f value for it         
def set_and_calculate_f_up(parent, up, goal_cell):
    parent.up = up
    # get new f, g and h
    new_g, new_h, new_f = calculate_f(up, parent, goal_cell)
    # set g, h, f or update them
    if up.f == sys.maxsize or up.f > new_f:
        set_g_h_f(up,new_g, new_h)

#####################################  LEFT CHILD CONDITIONS #####################################
# here we check the left child is unblocked or not and it is in closed list or not
def left_child_condition(parent, goal_cell, closed_list, opened_list):
     # make minimum_f_cost's left child if it is existed
    if parent.is_unblocked_left():
        # create left child
        left = cells[parent.row][parent.column - 1]

        if left not in closed_list:
            set_and_calculate_f_left(parent, left, goal_cell)
            opened_list.append(left)
            parent.left = left



# here we set left child and set or update g, h and f value for it          
def set_and_calculate_f_left(parent, left, goal_cell):
    parent.left = left
    # get new f, g and h
    new_g, new_h, new_f = calculate_f(left, parent, goal_cell)
    # set g, h, f or update them
    if left.f == sys.maxsize or left.f > new_f:
        set_g_h_f(left,new_g, new_h)

#####################################  RIGHT CHILD CONDITIONS #####################################
# here we check the right child is unblocked or not and it is in closed list or not
def right_child_condition(parent, goal_cell, closed_list, opened_list):
     # make minimum_f_cost's right child if it is existed
    if parent.is_unblocked_right():
        # create right child
        right = cells[parent.row][parent.column + 1]

        if right not in closed_list:
            set_and_calculate_f_right(parent, right, goal_cell)
            opened_list.append(right)
            parent.right = right



# here we set right child and set or update g, h and f value for it          
def set_and_calculate_f_right(parent, right, goal_cell):
    parent.right = right
    # get new f, g and h
    new_g, new_h, new_f = calculate_f(right, parent, goal_cell)
    # set g, h, f or update them
    if right.f == sys.maxsize or right.f > new_f:
        set_g_h_f(right,new_g, new_h)

#####################################  DOWN CHILD CONDITIONS #####################################
# here we check the DOWN child is unblocked or not and it is in closed list or not
def down_child_condition(parent, goal_cell, closed_list, opened_list):
     # make minimum_f_cost's down child if it is existed
    if parent.is_unblocked_down():
        # create down child
        down = cells[parent.row + 1][parent.column]
        if down not in closed_list:
            set_and_calculate_f_down(parent, down, goal_cell)
            opened_list.append(down)
            parent.down = down


# here we set down child and set or update g, h and f value for it          
def set_and_calculate_f_down(parent, down, goal_cell):
    parent.down = down
    # get new f, g and h
    new_g, new_h, new_f = calculate_f(down, parent, goal_cell)
    # set g, h, f or update them
    if down.f == sys.maxsize or down.f > new_f:
        set_g_h_f(down,new_g, new_h)


def calculate_f(child, parent, goal_cell):
    # calculate g
    # if there i no parent initialize the g with 0
    if parent is None:
        g = 0
    else:
        g = int(parent.distance_from_start_cell) + 1
    # # calculate h
    h = heuristic(goal_cell.row, goal_cell.column, child)
    # calculate f = g + h
    f = g + h
    return g, h, f
    

def set_g_h_f(cell, g, h):
    # set g
    cell.distance_from_start_cell = g
    # set h
    cell.distance_from_end_cell = h
    # set f
    cell.f = g + h


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
                total_cost = a_star_search(current_cell, Cell(0,0))
    is_solved = is_puzzle_solved(final_cells)
    depth = find_depth(cells)
    result = (total_cost, nodes_counter, actions, is_solved,cells,final_cells, depth)
    nodes_counter = 0
    actions = ''
    return result


def determine_heuristic(heuristic_type):
    global heuristic
    if heuristic_type == 'first':
        heuristic = first_heuristic
    elif heuristic_type == 'second':
        heuristic = second_heuristic
    elif heuristic_type == 'third':
        heuristic = third_heuristic


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

    
heuristic = third_heuristic
c = [[Cell(0,0,2), Cell(0,1,3)], [Cell(1,0,1), Cell(1,1,0)]]
total_cost = 0
for i in range(2):
    for j in range(2):
        current_cell = c[i][j]
        current_cell.distance_from_start_cell = 0
        if current_cell.value == 0:
            total_cost = a_star_search(current_cell, Cell(0,0))
print(total_cost)
