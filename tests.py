from puzzle import get_valid_moves, is_solved, heuristic, successors, State
from puzzle import PUZZLE_SIZE, SOLUTION, UP, DOWN, LEFT, RIGHT
from contextlib import redirect_stdout
import sys


def test_get_valid_moves():
    # upper row
    check(get_valid_moves(0, 0) == [DOWN, RIGHT], "get_valid_moves(0, 0)")
    check(
        get_valid_moves(0, PUZZLE_SIZE - 1) == [DOWN, LEFT],
        f"get_valid_moves(0, {PUZZLE_SIZE - 1})",
    )
    for col in range(1,PUZZLE_SIZE -1):
        check(
            get_valid_moves(0, col) == [DOWN, LEFT, RIGHT],
            f"get_valid_moves(0, {col})",
        )

    # lower row
    check(
        get_valid_moves(PUZZLE_SIZE - 1, 0) == [UP, RIGHT],
        f"get_valid_moves({PUZZLE_SIZE - 1}, 0)",
    )
    check(
        get_valid_moves(PUZZLE_SIZE - 1, PUZZLE_SIZE - 1) == [UP, LEFT],
        f"get_valid_moves({PUZZLE_SIZE - 1}, {PUZZLE_SIZE - 1})",
    )
    for col in range(1,PUZZLE_SIZE -1):
        check(
            get_valid_moves(PUZZLE_SIZE - 1, col) == [UP, LEFT, RIGHT],
            f"get_valid_moves({PUZZLE_SIZE - 1}, {col})",
        )

    # right col
    for row in range(1,PUZZLE_SIZE -1):
        check(
            get_valid_moves(row, 0) == [UP, DOWN, RIGHT],
            f"get_valid_moves({row}, 0)",
        )

    # left col
    for row in range(1,PUZZLE_SIZE -1):
        check(
            get_valid_moves(row, PUZZLE_SIZE - 1) == [UP, DOWN, LEFT],
            f"get_valid_moves({row}, {PUZZLE_SIZE - 1})",
        )

    # middle positions
    for row in range(1,PUZZLE_SIZE -1):
        for col in range(1,PUZZLE_SIZE -1):
            check(
                get_valid_moves(row, col) == [UP, DOWN, LEFT, RIGHT],
                f"get_valid_moves({row}, {col})",
            )

def test_is_solved():
    # test the solved state
    check(is_solved(SOLUTION) == True, "is_solved(SOLUTION)")

    # test an unsolved state
    unsolved_state = [row[:] for row in SOLUTION]
    unsolved_state[0][0], unsolved_state[0][1] = unsolved_state[0][1], unsolved_state[0][0]
    check(is_solved(unsolved_state) == False, "is_solved(unsolved_state)")

def test_heuristic():
    # test the heuristic function with a solved state
    check(heuristic(SOLUTION) == 0, "heuristic(SOLUTION)")

    # test the heuristic function with an unsolved state
    unsolved_board = [row[:] for row in SOLUTION]
    unsolved_board[0][0], unsolved_board[0][1] = unsolved_board[0][1], unsolved_board[0][0]
    check(heuristic(unsolved_board) == 2, "heuristic(unsolved_board)")

def test_successors():
    initial_board = [
        [row * PUZZLE_SIZE + col for col in range(PUZZLE_SIZE)]
        for row in range(PUZZLE_SIZE)
    ]
    state = State(initial_board, 0, heuristic(initial_board), None)
    successor_states = successors(state)

    # check that the number of successors is correct
    check(len(successor_states) == 2, "len(successors(state))")
    # check that the moves are valid and lead to correct states
    expected_moves = {DOWN, RIGHT}
    actual_moves = {s.movement for s in successor_states}
    check(actual_moves == expected_moves, "successors(state) moves")

    initial_board = [
        [row * PUZZLE_SIZE + col for col in range(PUZZLE_SIZE-1, -1, -1)]
        for row in range(PUZZLE_SIZE-1, -1, -1)
    ]
    state = State(initial_board, 0, heuristic(initial_board), None)
    successor_states = successors(state)

    # check that the number of successors is correct
    check(len(successor_states) == 2, "len(successors(state))")
    # check that the moves are valid and lead to correct states
    expected_moves = {UP, LEFT}
    actual_moves = {s.movement for s in successor_states}
    check(actual_moves == expected_moves, "successors(state) moves")

def test_state_equality():
    board = [row[:] for row in SOLUTION]
    same_board = [row[:] for row in SOLUTION]
    other_board = [row[:] for row in SOLUTION]
    other_board[0][0], other_board[0][1] = other_board[0][1], other_board[0][0]

    base = State(board, 0, heuristic(board))
    # same board reached through a different path
    twin = State(same_board, 5, heuristic(same_board), UP, base)
    different = State(other_board, 0, heuristic(other_board))

    check(base == twin, "states with equal boards are equal")
    check(not (base == different), "states with different boards are not equal")
    check(base != different, "states with different boards compare as !=")
    check(twin in [different, base], "state is found in a list by board equality")
    check(different not in [base], "state is not found when no board matches")
    check(not (base == "not a state"), "state does not equal a non-state")
    check(hash(base) == hash(twin), "states with equal boards share a hash")
    check(len({base, twin}) == 1, "equal states collapse in a set")


class IndentedWriter:
    def __init__(self, stream):
        self.stream = stream
        self.at_line_start = True

    def write(self, text):
        for part in text.splitlines(keepends=True):
            if self.at_line_start and part.strip():
                self.stream.write("\t")
            self.stream.write(part)
            self.at_line_start = part.endswith("\n")
        return len(text)

    def flush(self):
        self.stream.flush()

def check(condition, description):
    GREEN = "\033[32m"
    RED = "\033[31m"
    RESET = "\033[0m"
    status = f"{GREEN}Passed{RESET}" if condition else f"{RED}Failed{RESET}"
    print(f"{description}: {status}")

if __name__ == "__main__":
    print("Running tests for get_valid_moves()...")
    with redirect_stdout(IndentedWriter(sys.stdout)):
        test_get_valid_moves()

    print ("Running tests for is_solved()...")
    with redirect_stdout(IndentedWriter(sys.stdout)):
        test_is_solved()

    print ("Running tests for heuristic()...")
    with redirect_stdout(IndentedWriter(sys.stdout)):
        test_heuristic()

    print ("Running tests for successors()...")
    with redirect_stdout(IndentedWriter(sys.stdout)):
        test_successors()

    print ("Running tests for State equality...")
    with redirect_stdout(IndentedWriter(sys.stdout)):
        test_state_equality()
        