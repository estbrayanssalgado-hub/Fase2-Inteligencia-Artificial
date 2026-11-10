"""
Proyecto Integrador - Fase 2
Agente racional para la gestión inteligente del tráfico de red.

Modelo:
- Cada dispositivo de red es un nodo.
- Cada enlace es una arista no dirigida.
- El peso de cada arista representa un costo simplificado de transmisión
  (latencia + penalización por congestión), expresado en unidades de costo.
- BFS y DFS buscan rutas por número de enlaces.
- A* busca una ruta de costo mínimo usando una heurística admisible.

Ejecución:
    python main.py
"""

from collections import deque
from itertools import count
import heapq
import time
import csv
import statistics

# Grafo empresarial: 12 dispositivos.
# Los pesos son costos didácticos simulados, no mediciones de una red real.
GRAPH = {
    "R1":  {"SW1": 3, "SW2": 2},
    "SW1": {"R1": 3, "R2": 2, "R3": 2},
    "SW2": {"R1": 2, "R3": 2, "SW3": 2},
    "R2":  {"SW1": 2, "SW4": 2, "SW5": 6},
    "R3":  {"SW1": 2, "SW2": 2, "SW4": 3, "R4": 2},
    "SW3": {"SW2": 2, "R4": 2},
    "SW4": {"R2": 2, "R3": 3, "SW5": 2, "SW6": 2},
    "R4":  {"R3": 2, "SW3": 2, "SW6": 2},
    "SW5": {"R2": 6, "SW4": 2, "R5": 2},
    "SW6": {"SW4": 2, "R4": 2, "R5": 2},
    "R5":  {"SW5": 2, "SW6": 2, "S1": 2},
    "S1":  {"R5": 2},
}

# Coordenadas abstractas de la topología.
# h(n) = distancia Manhattan hasta S1. Cada arista tiene costo >=
# distancia Manhattan entre sus extremos; por ello h no sobreestima
# el costo real restante y es admisible.
COORDS = {
    "R1": (0, 0), "SW1": (1, 0), "SW2": (0, 1),
    "R2": (2, 0), "R3": (1, 1), "SW3": (0, 2),
    "SW4": (2, 1), "R4": (1, 2), "SW5": (3, 1),
    "SW6": (2, 2), "R5": (3, 2), "S1": (4, 2),
}

START = "R1"
GOAL = "S1"


def path_cost(path):
    """Calcula el costo acumulado de una ruta."""
    return sum(GRAPH[a][b] for a, b in zip(path, path[1:]))


def bfs(graph, start, goal):
    """Búsqueda en anchura: encuentra una ruta con mínimo número de aristas."""
    frontier = deque([[start]])
    visited = {start}
    expanded = 0

    while frontier:
        path = frontier.popleft()
        node = path[-1]

        if node == goal:
            return path, expanded

        expanded += 1
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                frontier.append(path + [neighbor])

    return None, expanded


def dfs(graph, start, goal):
    """Búsqueda en profundidad iterativa con control de visitados."""
    frontier = [[start]]
    visited = {start}
    expanded = 0

    while frontier:
        path = frontier.pop()
        node = path[-1]

        if node == goal:
            return path, expanded

        expanded += 1
        # Se invierte para conservar el orden de inserción al usar una pila.
        for neighbor in reversed(list(graph[node])):
            if neighbor not in visited:
                visited.add(neighbor)
                frontier.append(path + [neighbor])

    return None, expanded


def heuristic(node, goal):
    """Distancia Manhattan: cota inferior del costo restante."""
    x1, y1 = COORDS[node]
    x2, y2 = COORDS[goal]
    return 2 * (abs(x1 - x2) + abs(y1 - y2))


def astar(graph, start, goal):
    """A*: minimiza el costo acumulado g(n) + heurística h(n)."""
    sequence = count()
    frontier = [(heuristic(start, goal), next(sequence), 0, start, [start])]
    best_cost = {start: 0}
    expanded = 0

    while frontier:
        f_score, _, g_score, node, path = heapq.heappop(frontier)

        # Descarta entradas antiguas de la cola de prioridad.
        if g_score != best_cost.get(node):
            continue

        if node == goal:
            return path, expanded

        expanded += 1

        for neighbor, edge_cost in graph[node].items():
            new_cost = g_score + edge_cost
            if new_cost < best_cost.get(neighbor, float("inf")):
                best_cost[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, goal)
                heapq.heappush(
                    frontier,
                    (priority, next(sequence), new_cost,
                     neighbor, path + [neighbor])
                )

    return None, expanded


def benchmark(repetitions=1000):
    """Mide tiempo promedio, nodos expandidos y costo de la solución."""
    algorithms = {
        "BFS": bfs,
        "DFS": dfs,
        "A*": astar,
    }
    results = []

    for name, algorithm in algorithms.items():
        durations = []
        final_path, final_expanded = None, 0

        for _ in range(repetitions):
            start_time = time.perf_counter()
            path, expanded = algorithm(GRAPH, START, GOAL)
            durations.append(time.perf_counter() - start_time)
            final_path, final_expanded = path, expanded

        results.append({
            "Algoritmo": name,
            "Ruta": " -> ".join(final_path) if final_path else "No encontrada",
            "Nodos_expandidos": final_expanded,
            "Costo_solucion": path_cost(final_path) if final_path else None,
            "Tiempo_promedio_ms": statistics.mean(durations) * 1000,
            "Repeticiones": repetitions,
        })

    return results


def main():
    results = benchmark()

    print(f"Origen: {START} | Destino: {GOAL}")
    print("Costos de enlace: unidades simuladas")
    print("-" * 92)
    print(f"{'Algoritmo':<12}{'Expandidos':<14}{'Costo':<10}{'Tiempo (ms)':<16}Ruta")
    print("-" * 92)

    for row in results:
        print(
            f"{row['Algoritmo']:<12}"
            f"{row['Nodos_expandidos']:<14}"
            f"{row['Costo_solucion']:<10}"
            f"{row['Tiempo_promedio_ms']:<16.6f}"
            f"{row['Ruta']}"
        )

    with open("resultados.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print("\\nResultados guardados en resultados.csv")


if __name__ == "__main__":
    main()
