"""Independent oracle: iterative DFS over bitmasks, no shared code with solver.py."""
import time

from solver import DESPLAZAMIENTOS, resolver
#%% notebook starts here


def oracle(n, start, order, closed=False, limit=10**8):
    """Full tree walk: returns the first tour found in `order` (or None) and the number of partial paths."""
    idx = lambda f, c: f * n + c
    nbrs = [[idx(f + a, c + b) for a, b in order if 0 <= f + a < n and 0 <= c + b < n]
            for f in range(n) for c in range(n)]
    s = idx(*start)
    full = (1 << n * n) - 1
    nodes = 0
    first = None
    stack = [(s, 1 << s, [s])]
    while stack:
        sq, mask, path = stack.pop()
        nodes += 1
        if nodes > limit:
            return None, nodes
        if mask == full:
            if (not closed or s in nbrs[sq]) and first is None:
                first = [divmod(p, n) for p in path]
            continue
        # push in reverse so the first neighbour is explored first
        for nb in reversed(nbrs[sq]):
            if not mask >> nb & 1:
                stack.append((nb, mask | 1 << nb, path + [nb]))
    return first, nodes
#%% notebook ends here


if __name__ == "__main__":
    rows = []
    for n, closed in [(1, False), (1, True), (2, False), (3, False), (4, False), (5, True), (5, False)]:
        for f in range(n):
            for c in range(n):
                t = time.time()
                first, nodes = oracle(n, (f, c), DESPLAZAMIENTOS, closed, limit=3_000_000)
                if first is None and nodes <= 3_000_000:
                    st, _, _, exp = resolver(n, (f, c), cerrado=closed, presupuesto=nodes + 1)
                    ok = st == "fracaso" and exp == nodes
                    rows.append((n, (f, c), closed, "fracaso", nodes, exp, ok))
                elif first is not None:
                    st, path, _, _ = resolver(n, (f, c), cerrado=closed, presupuesto=10**7)
                    ok = st == "éxito" and path == [tuple(p) for p in first]
                    rows.append((n, (f, c), closed, "éxito", "-", "-", ok))
    for r in rows:
        print(r)
    print("all ok:", all(r[-1] for r in rows), len(rows))
