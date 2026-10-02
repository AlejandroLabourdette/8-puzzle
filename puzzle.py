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

def heuristic(state):
    # The number of misplaced tiles (excluding the blank tile)
    misplaced_tiles = 0
    for row in range(PUZZLE_SIZE):
        for col in range(PUZZLE_SIZE):
            if state[row][col] != 0 and state[row][col] != SOLUTION[row][col]:
                misplaced_tiles += 1
    return misplaced_tiles

def a_star(initial_state):
    pending_states = [initial_state]
    reviewed_states = []
    level = {initial_state: 0}
    cost = {initial_state: level[initial_state] + heuristic(initial_state)}

    def expand(node):
        pass
    pass



