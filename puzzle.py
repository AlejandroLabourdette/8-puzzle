PUZZLE_SIZE = 3
SOLUTION = [[1,2,3],
            [8,0,4],
            [7,6,5]]

UP = 'U'
DOWN = 'D'
RIGHT = 'R'
LEFT = 'L'

class State:
    def __init__(self, board, g_score, h_score, movement = None, parent = None):
        self.board = board
        self.g_score = g_score
        self.h_score = h_score
        self.movement = movement
        self.parent = parent

    def f_score(self):
        return self.g_score + self.h_score

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

def is_solved(board):
    for row in range(PUZZLE_SIZE):
        for col in range(PUZZLE_SIZE):
            if board[row][col] != SOLUTION[row][col]:
                return False    
    return True

def heuristic(board) -> int:
    # The number of misplaced tiles (excluding the blank tile)
    misplaced_tiles = 0
    for row in range(PUZZLE_SIZE):
        for col in range(PUZZLE_SIZE):
            if board[row][col] != 0 and board[row][col] != SOLUTION[row][col]:
                misplaced_tiles += 1
    return misplaced_tiles

def successors(state: State):
    blank_row, blank_col = None, None
    # Find the position of the blank tile (0)
    for row in range(PUZZLE_SIZE):
        for col in range(PUZZLE_SIZE):
            if state.board[row][col] == 0:
                blank_row, blank_col = row, col
                break

    valid_moves = get_valid_moves(blank_row, blank_col)
    successor_states = []

    for move in valid_moves:
        new_board = [row[:] for row in state.board]  # Create a copy of the current state
        if move == UP:
            new_board[blank_row][blank_col], new_board[blank_row - 1][blank_col] = new_board[blank_row - 1][blank_col], new_board[blank_row][blank_col]
        elif move == DOWN:
            new_board[blank_row][blank_col], new_board[blank_row + 1][blank_col] = new_board[blank_row + 1][blank_col], new_board[blank_row][blank_col]
        elif move == LEFT:
            new_board[blank_row][blank_col], new_board[blank_row][blank_col - 1] = new_board[blank_row][blank_col - 1], new_board[blank_row][blank_col]
        elif move == RIGHT:
            new_board[blank_row][blank_col], new_board[blank_row][blank_col + 1] = new_board[blank_row][blank_col + 1], new_board[blank_row][blank_col]

        successor_states.append(State(new_board, state.g_score + 1, heuristic(new_board), move, state))

    return successor_states

def a_star(initial_board):
    initial_state = State(initial_board, 0, heuristic(initial_board))
    pending_states = [initial_state]
    reviewed_states = []

    def expand(state):
        pending_states.remove(state)
        reviewed_states.append(state)
        successor_states = successors(state)
        for successor_state in successor_states:
            if not (successor_state in reviewed_states 
                    or successor_state in pending_states):
                pending_states.append(successor_state)
            else:
                pass

    while len(pending_states) > 0:
        min_state = min(pending_states, key=lambda x: x.f_score)
        expand(min_state)


        





