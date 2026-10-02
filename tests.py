from puzzle import get_valid_moves, is_solved, heuristic
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
    # Test the solved state
    check(is_solved(SOLUTION) == True, "is_solved(SOLUTION)")

    # Test an unsolved state
    unsolved_state = [row[:] for row in SOLUTION]
    unsolved_state[0][0], unsolved_state[0][1] = unsolved_state[0][1], unsolved_state[0][0]
    check(is_solved(unsolved_state) == False, "is_solved(unsolved_state)")

def test_heuristic():
    # Test the heuristic function with a solved state
    check(heuristic(SOLUTION) == 0, "heuristic(SOLUTION)")

    # Test the heuristic function with an unsolved state
    unsolved_state = [row[:] for row in SOLUTION]
    unsolved_state[0][0], unsolved_state[0][1] = unsolved_state[0][1], unsolved_state[0][0]
    check(heuristic(unsolved_state) == 2, "heuristic(unsolved_state)")

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
        