import heapq, random

def inversions(s):
    t = [x for x in s if x]
    return sum(t[i] > t[j] for i in range(len(t)) for j in range(i + 1, len(t)))

def solvable(start, goal):
    # 3x3 (odd width): same inversion parity as the goal <=> same component
    return inversions(start) % 2 == inversions(goal) % 2

def successors(s):
    b = s.index(0); r, c = divmod(b, 3)
    for name, dr, dc in (('U',-1,0), ('D',1,0), ('L',0,-1), ('R',0,1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            t = list(s); n = nr*3 + nc
            t[b], t[n] = t[n], t[b]
            yield name, tuple(t)

def make_manhattan(goal):
    pos = {v: divmod(i, 3) for i, v in enumerate(goal)}
    def h(s):
        total = 0
        for i, v in enumerate(s):
            if v:
                r, c = divmod(i, 3)
                total += abs(r - pos[v][0]) + abs(c - pos[v][1])
        return total
    return h

def astar(start, goal):
    start, goal = tuple(start), tuple(goal)
    if sorted(start) != list(range(9)) or sorted(goal) != list(range(9)):
        raise ValueError("Boards must use each of 0..8 exactly once (0 = blank)")
    if not solvable(start, goal):
        return None                      # different component: no path exists

    h = make_manhattan(goal)
    g = {start: 0}
    parent = {start: (None, None)}
    P = [(h(start), start)]
    while P:
        f, u = heapq.heappop(P)
        if f > g[u] + h(u):              # stale heap entry
            continue
        if u == goal:
            path = []
            while parent[u][0] is not None:
                u, mv = parent[u]
                path.append(mv)
            return path[::-1]
        for mv, v in successors(u):
            new_g = g[u] + 1
            if v not in g or g[v] > new_g:
                g[v] = new_g
                parent[v] = (u, mv)
                heapq.heappush(P, (new_g + h(v), v))
    return None

# --- usage -------------------------------------------------------------
SLIDES_GOAL = (1,2,3, 
               8,0,4, 
               7,6,5)
STANDARD_GOAL = (1,2,3, 
                 4,5,6, 
                 7,8,0)

# Guaranteed-solvable test: scramble by legal moves from the goal
def scramble(goal, n=40):
    s = tuple(goal)
    for _ in range(n):
        s = random.choice(list(successors(s)))[1]
    return s

if __name__ == "__main__":
    print(astar((2,8,3, 1,6,4, 7,0,5), SLIDES_GOAL))     # ['U','U','L','D','R']

    start = scramble(STANDARD_GOAL)
    print(start, astar(start, STANDARD_GOAL))

    # Swapping two tiles breaks parity -> unsolvable
    print(astar((2,1,3, 4,5,6, 7,8,0), STANDARD_GOAL))   # None
