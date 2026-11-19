# Taller IA: Backtracking y el recorrido del caballo

Santiago Valencia León (C.C. 1032797866) y Juan Manuel Galvis (C.C. 1004520611).

El cuaderno `Backtracking_Recorrido_del_Caballo.ipynb` ya está ejecutado: para revisarlo basta abrirlo,
no hace falta ejecutar nada. Nuestra solución está debajo de cada parte del enunciado, después de una
celda **SOLUCIÓN**.

`ejercicios_a_mano/` tiene la traza manual anotada, la pila de llamadas y el tablero bicolor. Hay dos
versiones del mismo dibujo:

- `ejercicios_a_mano.excalidraw`: se abre en https://excalidraw.com (menú > Open).
- `ejercicios-a-mano.excalidraw.md`: para Obsidian con el plugin Excalidraw.

## Ejecutarlo

Abrir el cuaderno y usar **Kernel > Restart Kernel and Run All Cells**. Tarda menos de un minuto y usa
unos 650 MB de memoria.

### Linux

```
python3 -m venv .venv
source .venv/bin/activate
pip install jupyterlab matplotlib pillow pandas
jupyter lab
```

### Windows

1. Instalar Python 3.12 o más nuevo desde https://www.python.org/downloads/ marcando
   **"Add python.exe to PATH"**.
2. En esta carpeta: clic derecho > **Abrir en Terminal**.
3. Ejecutar:
   ```
   py -m pip install jupyterlab matplotlib pillow pandas
   py -m jupyter lab
   ```
   (si `py` no existe, usar `python`).

Los resultados (estados, expansiones, retrocesos, trazas) salen iguales en cualquier máquina; solo
cambian los tiempos.
