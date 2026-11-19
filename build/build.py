"""Teacher notebook (verbatim) + our cells from parts.py, each group inserted after its teacher cell."""
import json
import re
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent
TEACHER = ROOT / "material_profesor/Backtracking_Recorrido_del_Caballo.ipynb"
OUT = ROOT / "Backtracking_Recorrido_del_Caballo.ipynb"


def module_body(name):
    text = (HERE / name).read_text()
    text = text.split("#%% notebook starts here\n", 1)[1]
    return text.split("#%% notebook ends here", 1)[0].strip("\n")


def cell(kind, text):
    if kind == "markdown":
        return {"cell_type": "markdown", "metadata": {}, "source": text}
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": text}


def parse_parts():
    groups, current, kind, lines = {}, None, None, []

    def flush():
        if kind:
            groups[current].append(cell(kind, "\n".join(lines).strip("\n")))

    for line in (HERE / "parts.py").read_text().splitlines():
        m = re.match(r"#%% (after (\d+)|md|code(?: (\w+))?)$", line)
        if not m:
            lines.append(line)
            continue
        flush()
        lines = []
        if m.group(2):
            current, kind = int(m.group(2)), None
            groups[current] = []
        elif m.group(1) == "md":
            kind = "markdown"
        else:
            kind = "code"
            if m.group(3):
                lines = [module_body(m.group(3) + ".py")]
    flush()
    return groups


teacher = json.loads(TEACHER.read_text())
groups = parse_parts()
cells = []
for i, c in enumerate(teacher["cells"]):
    cells.append(c)
    cells.extend(groups.get(i, []))
nb = dict(teacher, cells=cells)
nb["metadata"] = {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                  "language_info": {"name": "python"}}
OUT.write_text(json.dumps(nb, ensure_ascii=False, indent=1))
print(f"{OUT.name}: {len(teacher['cells'])} teacher cells + {len(cells) - len(teacher['cells'])} ours")
