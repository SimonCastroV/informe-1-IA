import math
import heapq
from typing import Tuple, List, Dict, Optional, Set

#Nodo para A*: guarda posición, padre, acción y costos (g, h, f)
class Node:
    def __init__(self, position: Tuple[int,int], parent=None, action: Optional[str]=None,
                 g: float=0.0, h: float=0.0):
        self.position = position
        self.parent = parent
        self.action = action
        self.g = g              #Costo acumulado desde el inicio
        self.h = h              #Heurística hasta la meta
        self.f = g + h          #Evaluación total

    def __lt__(self, other):
        if self.f == other.f:
            return self.g < other.g
        return self.f < other.f

class Problem:
    """
    Estructura del problema de laberinto:
    - state: tupla (fila, columna)
    - actions: dict(nombre -> delta de movimiento)
    - result(state, action) -> nuevo estado
    - action_cost(s, a, s2) -> costo de moverse al estado destino
    """
    def __init__(self, maze: List[List[str]],
                 start: Tuple[int,int]=None,
                 goals: Optional[Set[Tuple[int,int]]]=None,
                 terrain_cost: Optional[Dict[str,float]]=None,
                 impassable: Optional[Set[str]]=None):
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0]) if self.rows else 0

        #Detecta "S" y todas las "E" si no se pasan textualmente
        if start is None:
            start = self._find_unique('S')
        if goals is None:
            goals = set(self._find_all('E'))
        self.initial = start
        self.goals = goals

        #Acciones ortogonales es decir sin las diagonales
        self.actions = {
            'Up':    (-1,  0),
            'Down':  ( 1,  0),
            'Left':  ( 0, -1),
            'Right': ( 0,  1),
        }

        #Costos por tipo de celda
        self.terrain_cost = {
            ' ': 1.0,  #Libre
            'S': 1.0,  #Inicio
            'E': 1.0,  #Salida
            'M': 3.0,  #Barro
            'W': 5.0,  #Agua
        }
        if terrain_cost:
            self.terrain_cost.update(terrain_cost)

        #Paredes
        self.impassable = {'#'}
        if impassable:
            self.impassable |= set(impassable)

    #Busca una única aparición (Una sola "S")
    def _find_unique(self, ch: str) -> Tuple[int,int]:
        for r in range(self.rows):
            for c in range(self.cols):
                if self.maze[r][c] == ch:
                    return (r, c)
        raise ValueError(f"No se encontró el símbolo requerido '{ch}' en el laberinto.")

    #Devuelve todas las posiciones "E"
    def _find_all(self, ch: str) -> List[Tuple[int,int]]:
        res = []
        for r in range(self.rows):
            for c in range(self.cols):
                if self.maze[r][c] == ch:
                    res.append((r, c))
        return res

    #Valida que una posición esté dentro del tablero
    def in_bounds(self, pos: Tuple[int,int]) -> bool:
        r,c = pos
        return 0 <= r < self.rows and 0 <= c < self.cols

    #Verifica que no sea pared
    def passable(self, pos: Tuple[int,int]) -> bool:
        r,c = pos
        return self.maze[r][c] not in self.impassable

    #Aplica una acción a un estado y devuelve el nuevo estado
    def result(self, state: Tuple[int,int], action: str) -> Tuple[int,int]:
        dr, dc = self.actions[action]
        nr, nc = state[0] + dr, state[1] + dc
        return (nr, nc)

    #Costo de entrar a la celda destino, dependiendo el terreno
    def action_cost(self, s: Tuple[int,int], a: str, s2: Tuple[int,int]) -> float:
        cell = self.maze[s2[0]][s2[1]]
        return self.terrain_cost.get(cell, float('inf'))

    #Genera vecinos válidos (acción, nuevo_estado)
    def neighbors(self, state: Tuple[int,int]) -> List[Tuple[str,Tuple[int,int]]]:
        res = []
        for a, (dr,dc) in self.actions.items():
            nr, nc = state[0] + dr, state[1] + dc
            np = (nr, nc)
            if self.in_bounds(np) and self.passable(np):
                res.append((a, np))
        return res

#Heurística Manhattan: suma de distancias en filas y columnas a la meta más cercana
def h_manhattan(p: Tuple[int,int], goals: Set[Tuple[int,int]]) -> float:
    return min(abs(p[0]-gr) + abs(p[1]-gc) for gr,gc in goals)

#Heurística Euclidiana: distancia en línea recta a la meta más cercana
def h_euclidean(p: Tuple[int,int], goals: Set[Tuple[int,int]]) -> float:
    return min(math.hypot(p[0]-gr, p[1]-gc) for gr,gc in goals)

#Implementación de A* con soporte para múltiples metas
def astar(problem: Problem, heuristic: str = 'manhattan'):
    #Elige la heurística
    h = h_manhattan if heuristic == 'manhattan' else h_euclidean

    start = problem.initial
    goals = problem.goals

    #Nodo inicial
    start_node = Node(start, parent=None, action=None, g=0.0, h=h(start, goals))
    frontier = []
    heapq.heappush(frontier, start_node)

    reached: Dict[Tuple[int,int], float] = {start: 0.0}

    while frontier:
        current = heapq.heappop(frontier)

        if current.position in goals:
            return reconstruct_path(current)

        for action, s2 in problem.neighbors(current.position):
            g2 = current.g + problem.action_cost(current.position, action, s2)
            if g2 < reached.get(s2, float('inf')):
                reached[s2] = g2
                node2 = Node(s2, parent=current, action=action, g=g2, h=h(s2, goals))
                heapq.heappush(frontier, node2)

    return None  #No hay solución alguna

#Reconstruye el camino desde la meta al inicio (acción, posición)
def reconstruct_path(node: Node) -> List[Tuple[Optional[str], Tuple[int,int]]]:
    path = []
    while node:
        path.append((node.action, node.position))
        node = node.parent
    path.reverse()
    return path

#Ejemplo 1: laberinto base
maze = [
    ["#", "#", "#", "#", "#", "#", "#", "#"],
    ["#", "S", "#", " ", "#", " ", "E", "#"],
    ["#", " ", " ", " ", "#", " ", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "#"]
]

problem = Problem(maze)
sol = astar(problem, heuristic='manhattan')
print("Solución (acción, posición):")
print(sol)

#Ejemplo 2: múltiples salidas
maze_multi = [row[:] for row in maze]
maze_multi[2][6] = 'E'  # agrega otra salida
problem_multi = Problem(maze_multi)
sol_multi = astar(problem_multi, heuristic='euclidean')
print("\nSolución con múltiples E (euclidiana):")
print(sol_multi)

#Ejemplo 3: laberinto grande con obstáculos y costos
big_maze = [
    list("###############"),
    list("#S   M    #   #"),
    list("# ### ### # # #"),
    list("#   #   #   # #"),
    list("# W # ### ### #"),
    list("#   #   M   E #"),
    list("###############"),
]
problem_big = Problem(
    big_maze,
    terrain_cost={'M':3.0,'W':5.0,' ':1.0,'S':1.0,'E':1.0},
    impassable={'#'}
)
sol_big = astar(problem_big, heuristic='manhattan')
print("\nSolución en big_maze (con costos y obstáculos):")
print(sol_big)