"""Bugs the teacher's tests may miss, against our extra test (oracle existence + trace replay)."""
import json
from pathlib import Path

import solver
from oracle import oracle

SRC = Path(solver.__file__).read_text()
TESTS = "".join(json.loads((Path(__file__).parent.parent / "material_profesor/Backtracking_Recorrido_del_Caballo.ipynb").read_text())["cells"][11]["source"])
M = {
    "warnsdorff greedy": ("        for destino in candidates():\n",
                          "        for destino in (candidates()[:1] if estrategia == 'warnsdorff' else candidates()):\n"),
    "retreat logs return square": ("        traza.append((\"retroceso\", *square))\n",
                                   "        traza.append((\"retroceso\", *camino[-1]))\n"),
    "degree counts visited": ("len(saltos_legales(n, d, visitadas | {d}, orden))", "len(saltos_legales(n, d, set(), orden))"),
}
EXISTS = {(f, c): oracle(5, (f, c), solver.DESPLAZAMIENTOS)[0] is not None for f in range(5) for c in range(5)}

for name, (old, new) in M.items():
    assert old in SRC, name
    env = {}
    exec(SRC.replace(old, new), env)
    exec(TESTS, env)
    r = []
    for t in ("probar_saltos", "probar_resolver"):
        try:
            env[t]()
            r.append("pass")
        except Exception:
            r.append("FAIL")
    bad = []
    for (f, c), exists in EXISTS.items():
        st, _, tr, _ = env["resolver"](5, (f, c), estrategia="warnsdorff", presupuesto=10**7)
        if exists != (st == "éxito"):
            bad.append((f, c, st))
        path = []
        for i, (t, a, b) in enumerate(tr):
            if t in ("inicio", "avance"):
                path.append((a, b))
            elif t == "retroceso":
                if path[-1] != (a, b):
                    bad.append(("incoherent", f, c, i))
                    break
                path.pop()
    print(name, r, "our test:", "FAIL " + str(bad[:3]) if bad else "pass")
