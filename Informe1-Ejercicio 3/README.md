# Comparativa BFS vs IDS en la Red de Metro

## Resultados (A → J)

**Ruta encontrada:** `A → C → F → J`  
**Número de paradas:** 3

---

## Diferencias encontradas

### 1. Ruta encontrada
- Ambos métodos encontraron exactamente la misma ruta óptima: `A → C → F → J` con **3 paradas**.
- Esto era esperado porque el grafo es no ponderado y ambos algoritmos, en estas condiciones, pueden hallar rutas mínimas en número de pasos.

### 2. Nodos expandidos
- **BFS:** expandió **9** nodos.
- **IDS:** expandió **19** nodos.
- La diferencia se debe a que **IDS** reexplora los mismos nodos varias veces: primero busca con profundidad 0, luego 1, luego 2… hasta llegar a la profundidad solución (3 en este caso). En cada iteración vuelve a recorrer parte del grafo.

### 3. Máxima frontera
- **BFS:** tuvo una frontera máxima de **4** nodos.
- **IDS:** solo **3** nodos en memoria a la vez.
- Esto confirma que **IDS** usa menos memoria pico, ya que se comporta como una búsqueda en profundidad (guarda solo la rama actual y algunos nodos pendientes).

### 4. Tiempo de ejecución
- Ambos fueron extremadamente rápidos en este grafo pequeño: BFS ~0.177 ms, IDS ~0.141 ms.
- En este caso la diferencia de tiempo no es significativa, pero en grafos más grandes **IDS** puede ser más lento por la reexploración de niveles, mientras que BFS explora cada nodo una sola vez.

### 5. Uso de memoria
- **BFS:** ~4 KB.
- **IDS:** ~1 KB.
- Esto refleja que BFS almacena todos los nodos del nivel actual y próximos a expandir, mientras que IDS mantiene muy pocos nodos en memoria.

---

## Conclusión
- **BFS**: Ideal para encontrar la ruta más corta rápidamente en grafos pequeños o medianos, pero puede consumir mucha memoria en grafos grandes.
- **IDS**: Consume poca memoria y garantiza encontrar solución óptima en grafos no ponderados, pero a costa de reexplorar nodos y, en consecuencia, expandir más nodos y gastar más tiempo en general.

