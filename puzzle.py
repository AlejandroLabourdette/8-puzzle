PUZZLE_SIZE = 3
SOLUTION = [[1,2,3],
            [8,0,4],
            [7,6,5]]

UP = 'U'
DOWN = 'D'
RIGHT = 'R'
LEFT = 'L'


def get_valid_moves(row,col):
    if row == 0:
        if col == 0:
            return [DOWN, RIGHT]
        elif col == PUZZLE_SIZE-1:
            return [DOWN, LEFT]
        else:
            return [DOWN, LEFT, RIGHT]
    elif row == PUZZLE_SIZE-1:
        if col == 0:
            return [UP, RIGHT]
        elif col == PUZZLE_SIZE-1:
            return [UP, LEFT]
        else:
            return [UP, LEFT, RIGHT]
    elif col == 0:
        return [UP, DOWN, RIGHT]
    elif col == PUZZLE_SIZE-1:
        return [UP, DOWN, LEFT]
    else:
        return [UP, DOWN, LEFT, RIGHT]

def is_solved(state):
    for row in range(PUZZLE_SIZE):
        for col in range(PUZZLE_SIZE):
            if state[row][col] != SOLUTION[row][col]:
                return False    
    return True

def a_star():
    pending_states = []
    reviewed_states = []
    def expand(node):
        pass
    pass



