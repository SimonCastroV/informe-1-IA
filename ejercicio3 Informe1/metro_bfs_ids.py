from collections import deque
import time
import tracemalloc
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Set

# 1) Grafo (lista de adyacencia)
Graph: Dict[str, List[str]] = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B", "G"],
    "E": ["B", "H", "I"],
    "F": ["C", "J"],
    "G": ["D"],
    "H": ["E"],
    "I": ["E", "J"],
    "J": ["F", "I"],
}

# 2) Definiciones de Node y Problem
@dataclass
class Node:
    state: Any
    parent: Optional["Node"] = None
    action: Optional[Any] = None  # aquí action == estación a la que te mueves
    depth: int = 0
    def path(self) -> List[Any]:
        node, p = self, []
        while node:
            p.append(node.state)
            node = node.parent
        return list(reversed(p))

class Problem:
    def __init__(self, initial: Any, goal: Any, graph: Dict[Any, List[Any]]):
        self.initial = initial
        self.goal = goal
        self.graph = graph
    def actions(self, state: Any) -> List[Any]:
        return self.graph.get(state, [])
    def goal_test(self, state: Any) -> bool:
        return state == self.goal

# 3) BFS (óptimo en número de aristas con costo uniforme)
def bfs(problem: Problem) -> Tuple[Optional[Node], Dict[str, int]]:
    frontier = deque([Node(problem.initial)])
    explored: Set[Any] = set()
    metrics = {"expanded": 0, "max_frontier": 1}
    while frontier:
        metrics["max_frontier"] = max(metrics["max_frontier"], len(frontier))
        node = frontier.popleft()
        if problem.goal_test(node.state):
            return node, metrics
        if node.state in explored:
            continue
        explored.add(node.state)
        metrics["expanded"] += 1
        for action in problem.actions(node.state):
            if action not in explored and all(n.state != action for n in frontier):
                frontier.append(Node(action, node, action, node.depth + 1))
    return None, metrics

# 4) IDS (profundización iterativa con límite creciente)
def depth_limited_search(problem: Problem, limit: int, metrics: Dict[str, int]) -> Optional[Node]:
    stack = [Node(problem.initial)]
    visited_by_depth: Dict[Any, int] = {problem.initial: 0}
    while stack:
        node = stack.pop()
        if problem.goal_test(node.state):
            return node
        metrics["expanded"] += 1
        if node.depth < limit:
            for action in reversed(problem.actions(node.state)):  # para replicar orden recursivo
                new_depth = node.depth + 1
                if visited_by_depth.get(action, 10**9) > new_depth:
                    visited_by_depth[action] = new_depth
                    stack.append(Node(action, node, action, new_depth))
                    metrics["max_frontier"] = max(metrics["max_frontier"], len(stack))
    return None

def ids(problem: Problem, max_depth: int = 50) -> Tuple[Optional[Node], Dict[str, int], int]:
    metrics_total = {"expanded": 0, "max_frontier": 1}
    for limit in range(max_depth + 1):
        result = depth_limited_search(problem, limit, metrics_total)
        if result is not None:
            return result, metrics_total, limit
    return None, metrics_total, max_depth

# 5) Utilidad para medir tiempo y memoria
def run_with_metrics(search_fn, *args):
    tracemalloc.start()
    t0 = time.perf_counter()
    out = search_fn(*args)
    elapsed = (time.perf_counter() - t0) * 1000.0  # ms
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return out, elapsed, peak  # bytes

# 6) Ejecutar A -> J y comparar
def fmt_bytes(n: int) -> str:
    for unit in ["B","KB","MB","GB"]:
        if n < 1024:
            return f"{n:.0f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"

def show_result(name: str, node: Optional[Node], metrics: Dict[str, int], time_ms: float, mem_b: int, extra: str = ""):
    if node:
        path = node.path()
        print(f"{name} ✓")
        print(f"  Ruta encontrada: {' -> '.join(path)}")
        print(f"  Paradas (aristas): {len(path)-1}")
    else:
        print(f"{name} ✗  (no encontró ruta)")
    print(f"  Nodos expandidos: {metrics.get('expanded', 0)}")
    print(f"  Máx. frontera:    {metrics.get('max_frontier', 0)}")
    print(f"  Tiempo:           {time_ms:.3f} ms")
    print(f"  Pico memoria:     {fmt_bytes(mem_b)}")
    if extra:
        print(f"  {extra}")
    print()

if __name__ == "__main__":
    problem = Problem("A", "J", Graph) #<--------Cambiar las dos letras por Estacion principal y objetivo, cada una respectivamente 
                                                #Ejemplo (si quieres ir de A --> F se deja en Problem("A","F", Graph )

    (bfs_result, bfs_metrics), bfs_time_ms, bfs_peak_b = run_with_metrics(bfs, problem)
    (ids_result, ids_metrics, depth_used), ids_time_ms, ids_peak_b = run_with_metrics(ids, problem)

    print("=== Comparación BFS vs IDS en la red de metro (A → J) ===\n")
    show_result("BFS", bfs_result, bfs_metrics, bfs_time_ms, bfs_peak_b)
    show_result("IDS", ids_result, ids_metrics, ids_time_ms, ids_peak_b, extra=f"Profundidad usada: {depth_used}")

    print("Conclusión rápida:")
    print("- Con costo uniforme (1 por arista), BFS devuelve siempre la ruta con menos paradas.")
    print("- IDS usa menos memoria pico pero reexplora niveles y suele expandir más nodos.")
