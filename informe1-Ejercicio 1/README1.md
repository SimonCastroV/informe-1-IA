##**Análisis del problema**

El problema consiste en encontrar la mejor ruta posible desde un punto inicial hasta un destino, evitando obstáculos y recorriendo la menor distancia o el menor costo posible. En pocas palabras, se trata de moverse de manera inteligente en un espacio determinado, aprovechando la información que tenemos para no dar pasos innecesarios.

##** Cómo se aplica A* **

El algoritmo A* funciona como un buscador que evalúa diferentes caminos, pero no lo hace al azar.
En cada paso, analiza cuánto hemos avanzado y estima cuánto falta por recorrer.
Para eso combina dos cosas:
El costo real recorrido hasta el momento.
Una estimación de lo que falta para llegar a la meta.
Con esta combinación, A* decide cuál es el siguiente punto más prometedor a visitar, avanzando de forma ordenada hasta encontrar el destino.


##**¿Por qué la ruta encontrada es óptima?**

A* no solo busca cualquier camino que llegue a la meta, sino que lo hace calculando siempre la opción más eficiente según la información disponible.
Si se utiliza una estimación adecuada (heurística admisible), el algoritmo garantiza que el primer camino que encuentra hasta el destino es el más corto o el de menor costo posible.