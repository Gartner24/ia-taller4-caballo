"""Which plausible bugs pass the teacher's tests, and does the oracle test catch them?"""
import json
from pathlib import Path

import solver
from oracle import oracle

SRC = Path(solver.__file__).read_text()
MUTANTS = {
    "no discard on retreat": ("        visitadas.discard(square)\n", ""),
    "budget check after advance": (
        "            if expansiones >= presupuesto:\n                return \"límite\"\n            advance(destino)\n",
        "            advance(destino)\n            if expansiones >= presupuesto:\n                return \"límite\"\n"),
    "warnsdorff unstable ties": ("destinos.sort(key=lambda d:", "destinos.sort(reverse=True, key=lambda d:"),
    "no retreat before limit": ("            retreat()\n            if estado == \"límite\":\n                return estado\n",
                                "            if estado == \"límite\":\n                return estado\n            retreat()\n"),
    "closed check ignored": ("\"éxito\" if not cerrado or es_salto(camino[-1], inicio)", "\"éxito\" if True"),
}
nb = json.loads((Path(__file__).parent.parent / "material_profesor/Backtracking_Recorrido_del_Caballo.ipynb").read_text())
TESTS = "".join(nb["cells"][11]["source"])


def oracle_test(env):
    for n in (3, 4):
        for f in range(n):
            for c in range(n):
                _, nodes = oracle(n, (f, c), env["DESPLAZAMIENTOS"])
                st, _, traza, exp = env["resolver"](n, (f, c), presupuesto=10**6)
                assert st == "fracaso" and exp == nodes, (n, f, c, exp, nodes)
                assert traza[-1] == ("fracaso", f, c)


for name, (old, new) in MUTANTS.items():
    assert old in SRC, name
    env = {}
    exec(SRC.replace(old, new), env)
    exec(TESTS, env)
    res = []
    for t in ("probar_saltos", "probar_resolver"):
        try:
            env[t](); res.append("pass")
        except Exception as e:
            res.append(f"FAIL({type(e).__name__})")
    try:
        oracle_test(env); o = "pass"
    except Exception as e:
        o = f"FAIL {e}"
    print(f"{name:28s} teacher={res} oracle={o}")
