DESPLAZAMIENTOS = (
    (-1, 2), (1, 2), (2, 1), (2, -1),
    (1, -2), (-1, -2), (-2, -1), (-2, 1),
)
#%% notebook starts here


def saltos_legales(n, posicion, visitadas, orden):
    """Devuelve las casillas libres alcanzables, en el orden recibido."""
    fila, columna = posicion
    destinos = []
    for df, dc in orden:
        destino = (fila + df, columna + dc)
        if 0 <= destino[0] < n and 0 <= destino[1] < n and destino not in visitadas:
            destinos.append(destino)
    return destinos


def es_salto(a, b):
    # Same as the statement's helper (Reto 3 cell); resolver needs it before that cell runs.
    return sorted((abs(a[0] - b[0]), abs(a[1] - b[1]))) == [1, 2]


def resolver(n, inicio, *, orden=DESPLAZAMIENTOS, estrategia="fijo",
             cerrado=False, presupuesto=50_000):
    """Devuelve estado, camino, traza y número de expansiones."""
    if not (isinstance(n, int) and n > 0):
        raise ValueError("n must be a positive integer")
    if not (0 <= inicio[0] < n and 0 <= inicio[1] < n):
        raise ValueError("start square is outside the board")
    if sorted(orden) != sorted(DESPLAZAMIENTOS):
        raise ValueError("orden must be a permutation of DESPLAZAMIENTOS")
    if estrategia not in ("fijo", "warnsdorff"):
        raise ValueError("estrategia must be 'fijo' or 'warnsdorff'")
    if not (isinstance(presupuesto, int) and presupuesto > 0):
        raise ValueError("presupuesto must be a positive integer")

    camino = [inicio]
    visitadas = {inicio}
    traza = [("inicio", *inicio)]
    expansiones = 0

    def advance(square):
        camino.append(square)
        visitadas.add(square)
        traza.append(("avance", *square))

    def retreat():
        square = camino.pop()
        visitadas.discard(square)
        traza.append(("retroceso", *square))
        # O(1) guard for visitadas == set(camino); the full check is in the Reto 2 solution
        assert len(visitadas) == len(camino)

    def candidates():
        destinos = saltos_legales(n, camino[-1], visitadas, orden)
        if estrategia == "warnsdorff":
            # sorted() is stable, so ties keep the received order
            destinos.sort(key=lambda d: len(saltos_legales(n, d, visitadas | {d}, orden)))
        return destinos

    def search():
        nonlocal expansiones
        expansiones += 1
        if len(camino) == n * n:
            return "éxito" if not cerrado or es_salto(camino[-1], inicio) else "fracaso"
        for destino in candidates():
            if expansiones >= presupuesto:
                return "límite"
            advance(destino)
            estado = search()
            if estado == "éxito":
                return estado
            retreat()
            if estado == "límite":
                return estado
        return "fracaso"

    estado = search()
    # search refers to itself through its closure; breaking that cycle frees long traces right away
    del search
    traza.append((estado, *camino[-1]))
    return estado, (list(camino) if estado == "éxito" else None), traza, expansiones
