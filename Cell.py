import sys

class Cell:
    MAX_ROW = 3
    MAX_COLUMN = 3
    def __init__(self, row, column, value = None):
        self.row = row
        self.column = column
        self.value = value
        self.distance_from_start_cell = None # g
        self.distance_from_end_cell = None # h
        self.left = None
        self.right = None
        self.down = None
        self.up = None
        self.f = sys.maxsize


    @staticmethod
    def is_valid(row, column):
        return 0 < column + 1 <= Cell.MAX_COLUMN \
               and 0 < row + 1 <= Cell.MAX_ROW

    # check the cell is destination or not
    def is_destination(self,goal_cell):
        return self.row == goal_cell.row and \
               self.column == goal_cell.column

    # check the left cell is blocked or not
    def is_unblocked_left(self):
        return self.is_valid(self.row,self.column - 1)

    # check the right cell is blocked or not
    def is_unblocked_right(self):
        return self.is_valid(self.row,self.column + 1)

    # check the below cell is blocked or not
    def is_unblocked_down(self):
        return self.is_valid(self.row + 1,self.column)

    # check the above cell is blocked or not
    def is_unblocked_up(self):
        return self.is_valid(self.row - 1,self.column)

def make_cells():
    cells = [[x for x in range(Cell.MAX_ROW)] for x in range(Cell.MAX_COLUMN)]
    return cells


def is_puzzle_solved(cells):
    

    if not cells[0][0].value == 0:
            return False
    elif not cells[0][1].value == 1:
            return False
    elif not cells[0][2].value == 2:
            return False
    elif not cells[1][0].value == 3:
            return False
    elif not cells[1][1].value == 4:
            return False
    elif not cells[1][2].value == 5:
            return False
    elif not cells[2][0].value == 6:
            return False
    elif not cells[2][1].value == 7:
            return False
    elif not cells[2][2].value == 8:
            return False
    return True

# determine the happend action after expand the node
def determine_action(parent, child):

    if parent.left == child:
        return 'LEFT -> '
    elif parent.right == child:
        return 'RIGHT -> '
    elif parent.up == child:
        return 'UP -> '
    elif parent.down == child:
        return 'DOWN -> '
    
    return 'BACK -> '


# with this method we can move in 8-puzzle
def move(child, parent, cells):
    child_i , child_j = child.row, child.column
    parent_i , parent_j = parent.row, parent.column
    # swap values
    cells[child_i][child_j].value , cells[parent_i][parent_j].value = cells[parent_i][parent_j].value ,cells[child_i][child_j].value

def find_depth(cells):
    return int(cells[0][0].distance_from_start_cell)

# save the happend action and move the cell accordding to it 
def save_and_move_action(parent, child, final_cells):
    action = ''
    if parent is not None:
        # save happend action
        action = determine_action(parent, child)
        # do happend move in 8-puzzle
        move(child, parent, final_cells)

    return child,action

