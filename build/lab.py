import json
from pathlib import Path

nb = json.loads((Path(__file__).parent.parent / "material_profesor/Backtracking_Recorrido_del_Caballo.ipynb").read_text())
env = {}
exec("".join(nb["cells"][3]["source"]), env)
T = env["TRAZA_DEMO"]
path = []
paths = []
for t, a, b in T:
    if t in ("inicio", "avance"):
        path.append((a, b))
    elif t == "retroceso":
        assert path[-1] == (a, b)
        path.pop()
    paths.append(list(path))
i = next(k for k, e in enumerate(T) if e[0] == "retroceso")
print("first retroceso idx", i, T[i], "before", len(paths[i - 1]), "after", len(paths[i]), "horse at", paths[i][-1])
print("events around", T[i - 2:i + 5])
print("last 3 before", paths[i - 1][-3:], "after", paths[i][-3:])
from solver import saltos_legales, DESPLAZAMIENTOS
for k in (i - 1, i):
    p = paths[k]
    for depth in range(len(p) - 3, len(p)):
        sq = p[depth]
        print(k, "level", depth + 1, sq, "cands", saltos_legales(5, sq, set(p[:depth + 1]), DESPLAZAMIENTOS))
freed = {}
for k, (t, a, b) in enumerate(T):
    if t == "retroceso":
        freed.setdefault((a, b), k)
    elif t == "avance" and (a, b) in freed:
        print("re-entered", (a, b), "freed at", freed[(a, b)], "re-added at", k, "prefix len", len(paths[k]), "prev at", paths[k][-2])
        break
print("total events", len(T), "avances", sum(e[0] == "avance" for e in T), "retrocesos", sum(e[0] == "retroceso" for e in T))
print("final path", paths[-1])
