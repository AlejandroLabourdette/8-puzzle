# Terminal visualizer for the A* search tree built by puzzle.a_star().
# Colors are raw ANSI escape codes, the same style already used in tests.py.

RESET = "\033[0m"
GRAY = "\033[90m"
YELLOW = "\033[33m"
GREEN = "\033[1;32m"
CLEAR_SCREEN = "\033[2J\033[H"

LAST_CONNECTOR = "└── "
MIDDLE_CONNECTOR = "├── "
LAST_PREFIX = "    "
MIDDLE_PREFIX = "│   "

def format_board(board) -> str:
    # [[2,8,3],[1,6,4],[7,0,5]] becomes "2,8,3|1,6,4|7,0,5"
    return "|".join(",".join(str(tile) for tile in row) for row in board)

def format_node(state) -> str:
    movement = state.movement if state.movement is not None else "-"
    return (f"{format_board(state.board)}  {movement}  "
            f"g={state.g_score} h={state.h_score} f={state.f_score()}")

def build_children_index(discovered_states):
    # Group the discovered states by the identity of their parent, so the tree can be
    # walked top down. Identity is used instead of equality because State.__eq__ only
    # compares boards, which would merge distinct nodes of the tree.
    children = {}
    for state in discovered_states:
        if state.parent is None:
            continue
        children.setdefault(id(state.parent), []).append(state)
    return children

def color_for(state, pending_ids, next_state) -> str:
    if state is next_state:
        return GREEN
    if id(state) in pending_ids:
        return YELLOW
    return GRAY

def print_branch(state, children, pending_ids, next_state, prefix, depth = 0) -> int:
    # Prints the subtree hanging from state and returns the deepest level reached,
    # measured in moves away from the root (so it matches the g scores on screen).
    max_depth = depth
    state_children = children.get(id(state), [])
    for index, child in enumerate(state_children):
        is_last = index == len(state_children) - 1
        connector = LAST_CONNECTOR if is_last else MIDDLE_CONNECTOR
        color = color_for(child, pending_ids, next_state)
        print(f"{prefix}{connector}{color}{format_node(child)}{RESET}")
        child_prefix = prefix + (LAST_PREFIX if is_last else MIDDLE_PREFIX)
        child_depth = print_branch(child, children, pending_ids, next_state,
                                   child_prefix, depth + 1)
        max_depth = max(max_depth, child_depth)
    return max_depth

def print_legend(explored_count, pending_count, tree_depth):
    print(f"{GRAY}explored ({explored_count}){RESET}  "
          f"{YELLOW}pending ({pending_count}){RESET}  "
          f"{GREEN}next to expand{RESET}  "
          f"depth ({tree_depth})")

def print_search_tree(root_state, reviewed_states, pending_states, next_state,
                      iteration, pause = True) -> bool:
    # Draw every discovered state as a tree and, when pause is on, wait for the user.
    # Returns False when the user asks to stop tracing (or stdin is not interactive),
    # so the caller can let the search finish silently.
    children = build_children_index(list(reviewed_states) + list(pending_states))
    pending_ids = {id(state) for state in pending_states}

    if pause:
        print(CLEAR_SCREEN, end="")
    print(f"Iteration {iteration}")
    print()
    root_color = color_for(root_state, pending_ids, next_state)
    print(f"{root_color}{format_node(root_state)}{RESET}")
    tree_depth = print_branch(root_state, children, pending_ids, next_state, "")
    print()
    print_legend(len(reviewed_states), len(pending_states), tree_depth)

    if not pause:
        return True
    try:
        answer = input("[Enter to continue, q to stop tracing] ")
    except (EOFError, KeyboardInterrupt):
        print()
        return False
    return answer.strip().lower() != "q"
