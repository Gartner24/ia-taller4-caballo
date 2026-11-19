"""Run the teacher's tests against solver.py and look for the order behind TRAZA_DEMO."""
import itertools
import json
import time
from pathlib import Path

from solver import DESPLAZAMIENTOS, resolver

nb = json.loads((Path(__file__).parent.parent / "material_profesor/Backtracking_Recorrido_del_Caballo.ipynb").read_text())
cells = ["".join(c["source"]) for c in nb["cells"]]
env = {"DESPLAZAMIENTOS": DESPLAZAMIENTOS, "resolver": resolver}
from solver import saltos_legales
env["saltos_legales"] = saltos_legales
exec(cells[11], env)
env["probar_saltos"]()
env["probar_resolver"]()
print("teacher tests pass")

exec(cells[3], env)
demo = env["TRAZA_DEMO"]
advances = sum(1 for e in demo if e[0] == "avance")
t = time.time()
matches = []
for perm in itertools.permutations(DESPLAZAMIENTOS):
    _, _, traza, _ = resolver(5, (0, 0), orden=perm, presupuesto=advances + 1)
    if traza == demo:
        matches.append(perm)
print(len(matches), "orders reproduce TRAZA_DEMO", round(time.time() - t, 1), "s")
for m in matches[:5]:
    print(m)

for est in ("fijo", "warnsdorff"):
    r = resolver(5, (0, 0), estrategia=est)
    print(est, r[0], r[3], sum(1 for e in r[2] if e[0] == "retroceso"))
