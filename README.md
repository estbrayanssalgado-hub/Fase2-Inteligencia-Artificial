# Fase 2 – Proyecto Integrador de Inteligencia Artificial

## Agente racional para la gestión inteligente del tráfico de red

Este proyecto modela una red empresarial como un grafo ponderado de 12 dispositivos. Cada dispositivo es un nodo y cada enlace es una arista. El peso de la arista representa un costo didáctico simulado de transmisión (latencia más penalización por congestión).

### Requisitos
- Python 3.9 o superior.
- No requiere instalar librerías externas.

### Ejecución
Desde la carpeta del proyecto, ejecutar:

```bash
python main.py
```

El programa ejecuta BFS, DFS y A* 1.000 veces, muestra la ruta encontrada, los nodos expandidos, el costo y el tiempo promedio. También genera `resultados.csv`.

### Algoritmos
- **BFS:** búsqueda no informada en anchura; encuentra una ruta con el menor número de enlaces.
- **DFS:** búsqueda no informada en profundidad; encuentra una ruta, pero no garantiza que sea de costo mínimo.
- **A*:** búsqueda informada que prioriza `f(n) = g(n) + h(n)` y minimiza el costo acumulado.

### Heurística de A*
Se utiliza `h(n) = 2 × distancia Manhattan(n, S1)`, calculada sobre coordenadas abstractas de la topología. Los costos de todos los enlaces son iguales o superiores a dos veces la distancia Manhattan entre sus extremos; por tanto, la heurística no sobreestima el costo real restante y es admisible. Además, es consistente.

### Resultados de referencia
Los tiempos dependen del equipo y del entorno de ejecución. Los valores del informe corresponden a una ejecución de referencia de 1.000 repeticiones. Vuelve a ejecutar el programa para obtener los valores de tu computador.

### Estructura
- `main.py`: implementación de BFS, DFS, A* y benchmark.
- `resultados.csv`: resultados de la ejecución de referencia.
- `informe_fase2.pdf`: documento técnico de la actividad.

**Nota:** La red, coordenadas y costos son una simulación determinista para fines académicos; no son mediciones de una infraestructura empresarial real.
