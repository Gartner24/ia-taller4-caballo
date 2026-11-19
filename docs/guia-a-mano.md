# Taller 4: qué hacer a mano

El enunciado pide tres cosas a mano. Todas están dibujadas en `ejercicios_a_mano.excalidraw` y resueltas en el cuaderno.

## 1. Traza manual anotada (sección 4, la piden en la entrega)

Copiar la tabla de los eventos 20 a 27 de la traza 5x5 desde (0, 0):

| Evento | Tipo | Casilla | Visitadas | Qué pasa |
|---:|---|---|---:|---|
| 20 | avance | (2, 2) | 21 | (3, 0) prueba su primer destino |
| 21 | avance | (0, 3) | 22 | único salto libre desde (2, 2) |
| 22 | avance | (1, 1) | 23 | único salto libre desde (0, 3) |
| 23 | retroceso | (1, 1) | 22 | (1, 1) sin salidas: se libera |
| 24 | retroceso | (0, 3) | 21 | (0, 3) sin alternativas |
| 25 | retroceso | (2, 2) | 20 | (2, 2) sin alternativas |
| 26 | avance | (1, 1) | 21 | (3, 0) prueba su segundo destino |
| 27 | avance | (0, 3) | 22 | misma casilla, otro camino |

## 2. Pila de llamadas (laboratorio, pregunta 2)

Dibujar dos columnas de cajas, el tope arriba:

```text
Antes (evento 22)                 Después (evento 23)
[23  (1, 1)  sin salidas]  <- tope
[22  (0, 3)  probando (1, 1)]     [22  (0, 3)  elige siguiente]  <- tope
[21  (2, 2)  probando (0, 3)]     [21  (2, 2)  probando (0, 3)]
                                  [20  (3, 0)  probando (2, 2)]
```

Al lado: "El marco que elige es el de (0, 3). No le quedan opciones, así que también retrocede (evento 24)."

## 3. Tablero bicolor (Reto 3, punto 3)

Dibujar un 5x5 de ajedrez y escribir: cada salto cambia de color; un recorrido cerrado tiene n² saltos; para volver al color del inicio hace falta un número par; con n impar, n² es impar: imposible.

## Para la sustentación

Cada uno debe poder:

- Reconstruir a mano un pedazo de traza (practicar con la tabla de arriba).
- Explicar una decisión: Santiago, por qué el presupuesto se revisa antes de cada avance; Juan Manuel, por qué solo `advance` y `retreat` tocan el camino.
- Predecir antes de correr: primer destino (primer salto del orden que cabe en el tablero), y con presupuesto p pequeño: límite, p expansiones, p - 1 retrocesos.
