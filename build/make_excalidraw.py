"""Write the hand exercises of Taller 4 as Excalidraw: .excalidraw.md (Obsidian) or .excalidraw (excalidraw.com)."""
import json
import random
import sys
from pathlib import Path

from solver import DESPLAZAMIENTOS

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent.parent / "docs" / "ejercicios-a-mano.excalidraw.md"
rng = random.Random(7)
elements = []
BLUE, GREEN, RED, ORANGE, GRAY, BLACK = "#1971c2", "#2f9e44", "#e03131", "#e8590c", "#868e96", "#1e1e1e"


def base(kind, x, y, w, h, color=BLACK, **kw):
    e = dict(id=f"e{len(elements)}", type=kind, x=x, y=y, width=w, height=h, angle=0, strokeColor=color,
             backgroundColor="transparent", fillStyle="solid", strokeWidth=2, strokeStyle="solid", roughness=1,
             opacity=100, groupIds=[], frameId=None, roundness=None, seed=rng.randrange(1, 2**31),
             version=1, versionNonce=rng.randrange(1, 2**31), isDeleted=False, boundElements=[], updated=1,
             link=None, locked=False)
    e.update(kw)
    elements.append(e)
    return e


def text(x, y, s, size=18, color=BLACK, mono=False, container=None, align="left"):
    lines = s.split("\n")
    w = max(len(l) for l in lines) * size * (0.6 if mono else 0.55)
    h = len(lines) * size * 1.25
    if container:
        x = container["x"] + (container["width"] - w) / 2
        y = container["y"] + (container["height"] - h) / 2
    e = base("text", x, y, w, h, color, text=s, originalText=s, fontSize=size, fontFamily=3 if mono else 1,
             textAlign=align, verticalAlign="middle", containerId=container["id"] if container else None,
             lineHeight=1.25, autoResize=True)
    if container:
        container["boundElements"].append({"type": "text", "id": e["id"]})
    return e


def box(x, y, w, h, label=None, color=BLACK, fill="transparent", size=18, shape="rectangle", rounded=True):
    b = base(shape, x, y, w, h, color, backgroundColor=fill, roundness={"type": 3} if rounded else None)
    if label is not None:
        text(0, 0, label, size, color, container=b, align="center")
    return b


def line(x1, y1, x2, y2, color=BLACK, arrow=False, dashed=False):
    return base("arrow" if arrow else "line", x1, y1, x2 - x1, y2 - y1, color, points=[[0, 0], [x2 - x1, y2 - y1]],
                startBinding=None, endBinding=None, startArrowhead=None, endArrowhead="arrow" if arrow else None,
                lastCommittedPoint=None, strokeStyle="dashed" if dashed else "solid", roundness={"type": 2})


def section(y, title):
    text(0, y, title, 30, BLUE)
    return y + 55


def board(x0, y0, n, cell, numbers=None, horse=None, cross=None, colors=False):
    """numbers: {(f, c): label}; horse/cross: squares highlighted in green/orange."""
    for i in range(n):
        text(x0 - 25, y0 + i * cell + cell / 2 - 11, str(i), 16, GRAY)
        text(x0 + i * cell + cell / 2 - 5, y0 - 28, str(i), 16, GRAY)
    for f in range(n):
        for c in range(n):
            fill = ("#f1f3f5" if (f + c) % 2 == 0 else "#adb5bd") if colors else "transparent"
            label, col = None, BLACK
            if numbers and (f, c) in numbers:
                fill, label = "#d3f9d8", str(numbers[(f, c)])
            if horse == (f, c):
                fill, col = "#b2f2bb", GREEN
            if cross == (f, c):
                fill, label, col = "#ffd8a8", "X", ORANGE
            box(x0 + c * cell, y0 + f * cell, cell, cell, label, col, fill, 16, rounded=False)


# ---------------------------------------------------------------- title
text(0, 0, "Taller 4 - Recorrido del caballo: ejercicios a mano", 40)
text(0, 60, "Santiago Valencia León (C.C. 1032797866) y Juan Manuel Galvis (C.C. 1004520611). "
            "Todo está también en el cuaderno, debajo de cada SOLUCIÓN.", 18, GRAY)
y = 130

# ---------------------------------------------------------------- Reto 1
y = section(y, "Reto 1. Saltos legales a mano")
rows = "\n".join(f"  {str(d):9s} -> {str((d[0], d[1])):9s} {'legal' if 0 <= d[0] < 5 and 0 <= d[1] < 5 else 'fuera'}"
                 for d in DESPLAZAMIENTOS)
text(0, y, "Desde (0, 0) en 5x5: sumar cada desplazamiento en orden\n\n" + rows +
     "\n\n  Resultado: [(1, 2), (2, 1)]   (en el orden de DESPLAZAMIENTOS)\n"
     "  Si (1, 2) ya está visitada: [(2, 1)]\n"
     "  Centro (2, 2): caben los 8 saltos\n"
     "  Tablero 2x2: ningún salto cabe -> []", 18, mono=True)
board(760, y + 40, 5, 50, numbers={(0, 0): "ini"}, horse=None)
for d in [(1, 2), (2, 1)]:
    box(760 + d[1] * 50, y + 40 + d[0] * 50, 50, 50, "ok", GREEN, "#b2f2bb", 16, rounded=False)
y += 420

# ---------------------------------------------------------------- Lab
y = section(y, "Sección 2. Laboratorio de observación (traza del docente, 5x5 desde (0, 0))")
text(0, y, "1. Primer retroceso = evento 23. Se libera (1, 1); el caballo vuelve a (0, 3).\n"
           "   Visitadas: 23 antes, 22 después. (1, 1) no tenía saltos libres.", 18)
y += 80
order = [(0, 0), (1, 2), (0, 4), (2, 3), (4, 4), (3, 2), (2, 4), (4, 3), (3, 1), (1, 0), (0, 2), (1, 4), (3, 3),
         (4, 1), (2, 0), (0, 1), (1, 3), (3, 4), (4, 2), (3, 0), (2, 2), (0, 3), (1, 1)]
text(0, y, "Tablero en el evento 22 (antes)", 18, GRAY)
board(30, y + 60, 5, 50, numbers={sq: i + 1 for i, sq in enumerate(order)}, horse=(1, 1))
text(380, y, "Tablero en el evento 23 (después)", 18, GRAY)
board(410, y + 60, 5, 50, numbers={sq: i + 1 for i, sq in enumerate(order[:-1])}, horse=(0, 3), cross=(1, 1))
text(720, y + 80, "El 23 desaparece de (1, 1) (aspa).\nEl caballo queda en (0, 3), con el 22.\n"
                  "El contador baja de 23 a 22.", 18)
y += 360

text(0, y, "2. Pila de llamadas (últimos tres niveles)", 22, GREEN)
y += 45
for dx, title, frames, top in [
    (0, "Justo antes (evento 22)", [("nivel 23  BUSCAR ... (1, 1)", "sin destinos libres: fracasa"),
                                     ("nivel 22  BUSCAR ... (0, 3)", "probando (1, 1)"),
                                     ("nivel 21  BUSCAR ... (2, 2)", "probando (0, 3)")], 0),
    (520, "Justo después (evento 23)", [("nivel 22  BUSCAR ... (0, 3)", "elige el siguiente destino"),
                                        ("nivel 21  BUSCAR ... (2, 2)", "probando (0, 3)"),
                                        ("nivel 20  BUSCAR ... (3, 0)", "probando (2, 2)")], 0)]:
    text(dx, y, title, 18, GRAY)
    for k, (head, note) in enumerate(frames):
        color = RED if (dx == 0 and k == 0) else (ORANGE if k == top else BLACK)
        box(dx, y + 35 + k * 80, 420, 70, head + "\n" + note, color,
            "#fff4e6" if k == top else "transparent", 18)
    text(dx + 430, y + 55, "<- tope", 18, ORANGE)
y += 300
text(0, y, "El marco que elige es el de (0, 3): él hizo el avance a (1, 1), lo deshace y sigue su ciclo.\n"
           "No le quedan opciones -> evento 24 retrocede (0, 3); igual (2, 2) en el 25;\n"
           "el marco de (3, 0) sí tiene otra: evento 26 avanza a (1, 1).", 18)
y += 100
text(0, y, "3. (1, 1) se libera en el evento 23 y vuelve en el 26 (desde (3, 0)). Es válido porque al retroceder se\n"
           "   quitó de camino y de visitadas: está libre. Y es otro camino (20 casillas antes, no 22): otro nodo.", 18)
y += 100

# ---------------------------------------------------------------- manual trace
y = section(y, "Sección 4. Traza manual anotada (eventos 20 a 27)")
text(0, y, "evento  tipo        casilla  visitadas  qué pasa\n"
           "  20    avance      (2, 2)      21      (3, 0) prueba su primer destino\n"
           "  21    avance      (0, 3)      22      único salto libre desde (2, 2)\n"
           "  22    avance      (1, 1)      23      único salto libre desde (0, 3)\n"
           "  23    retroceso   (1, 1)      22      (1, 1) sin salidas: se libera\n"
           "  24    retroceso   (0, 3)      21      (0, 3) sin alternativas\n"
           "  25    retroceso   (2, 2)      20      (2, 2) sin alternativas\n"
           "  26    avance      (1, 1)      21      (3, 0) prueba su segundo destino\n"
           "  27    avance      (0, 3)      22      misma casilla, otro camino", 18, mono=True)
y += 260

# ---------------------------------------------------------------- bicolor
y = section(y, "Reto 3.3. Por qué no hay recorrido cerrado en tablero impar")
board(30, y + 40, 5, 50, colors=True)
text(330, y + 30, "Clara: f + c par (13 casillas). Oscura: f + c impar (12).\n\n"
                  "1. Un salto mueve 1 + 2 = 3 casillas (impar): siempre cambia de color.\n"
                  "2. Cerrado = n² saltos contando el regreso al inicio.\n"
                  "3. Volver al color del inicio pide un número PAR de saltos.\n"
                  "4. n impar -> n² impar -> se termina en el otro color. Imposible.\n\n"
                  "1x1: n² = 1, el regreso sería (0, 0) -> (0, 0): no es salto. Fracaso.\n"
                  "Abierto en 5x5: 25 casillas alternan colores -> 13 de un color y 12 del otro.\n"
                  "Hay que empezar en clara. Desde oscura: fracaso (el cuaderno lo comprueba).", 18)
y += 330

# ---------------------------------------------------------------- Reto 4
y = section(y, "Reto 4. Nuestra rama fallida (6x6, inicio (0, 1), rotación 7, fijo)")
text(0, y, "Orden rotado: (-2, 1) (-1, 2) (1, 2) (2, 1) (2, -1) (1, -2) (-1, -2) (-2, -1)\n\n"
           "Evento 25: el caballo llega a (5, 5) con 26 casillas visitadas.\n"
           "(5, 5) solo salta a (3, 4) y (4, 3), y las dos ya están en el camino.\n"
           "Evento 26: retroceso. Se libera (5, 5); el caballo queda en (4, 3).\n"
           "Evento 27: el marco de (4, 3) sigue con su ciclo: el siguiente libre es (2, 2).", 18)
y += 200

# ---------------------------------------------------------------- oral
y = section(y, "Para la sustentación: anticipar antes de ejecutar")
text(0, y, "Primer destino: recorrer el orden y quedarse con el primer salto que cae dentro del tablero.\n"
           "  Ej.: (0, 1) en 6x6 con rotación 7: (-2, 1) fuera, (-1, 2) fuera, (1, 2) -> (1, 3).\n"
           "  Si cambian (1, 2) por (2, 1): el primero que cabe es (2, 1) -> (2, 2).\n\n"
           "Presupuesto p menor que el que necesita la búsqueda:\n"
           "  estado límite, p expansiones, p - 1 retrocesos, camino None, último evento (límite, inicio).\n"
           "  p = 1: traza [inicio, límite].   p = 2: [inicio, avance, retroceso, límite].\n\n"
           "Éxito: retrocesos = expansiones - n².     Límite: retrocesos = expansiones - 1.\n"
           "Cerrado con n impar: imposible (fracaso o límite, nunca éxito).", 18, mono=True)

doc = {"type": "excalidraw", "version": 2, "source": "https://github.com/zsviczian/obsidian-excalidraw-plugin",
       "elements": elements, "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff"}, "files": {}}
if OUT.suffix == ".excalidraw":   # plain file for excalidraw.com (File > Open)
    OUT.write_text(json.dumps({**doc, "source": "https://excalidraw.com"}, ensure_ascii=False, indent=1))
    print(f"{len(elements)} elements -> {OUT}")
    sys.exit()
texts = "\n".join(f"{e['text']} ^{e['id']}\n" for e in elements if e["type"] == "text")
OUT.write_text("---\n\nexcalidraw-plugin: parsed\ntags: [excalidraw]\n\n---\n"
               "==⚠  Switch to EXCALIDRAW VIEW in the MORE OPTIONS menu of this document. ⚠==\n\n\n"
               "# Excalidraw Data\n\n## Text Elements\n" + texts + "\n%%\n## Drawing\n```json\n"
               + json.dumps(doc, ensure_ascii=False, indent=1) + "\n```\n%%")
print(f"{len(elements)} elements -> {OUT}")
