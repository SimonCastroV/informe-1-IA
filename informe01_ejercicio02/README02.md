1. Resolver el ejercicio planteado
El código ya resuelve el problema del laberinto usando el algoritmo A* con diferentes heurísticas y configuraciones de laberinto, mostrando la solución paso a paso para cada caso

2. ¿Cómo cambia el comportamiento del algoritmo si cambiamos la función de costo?
Si cambias la función de costo (por ejemplo, asignando valores más altos a ciertos terrenos como 'M' para barro o 'W' para agua), el algoritmo A* preferirá caminos que eviten esos terrenos costosos, aunque sean más largos en distancia. Así, el camino óptimo puede cambiar dependiendo de los costos asignados a cada tipo de celda

3. ¿Qué sucede si hay múltiples salidas en el laberinto? ¿Cómo podrías modificar el algoritmo para manejar esto? Plantea una propuesta.
El código ya soporta múltiples salidas: el algoritmo termina cuando alcanza cualquiera de las posiciones marcadas como 'E'. Para manejar esto, basta con definir todas las salidas en el conjunto de metas (goals). No es necesario modificar el algoritmo, solo asegurarse de que todas las salidas estén incluidas en el conjunto de metas al crear el problema

4. Modifica el laberinto por uno más grande y con otro tipo de obstáculo además de paredes. ¿Qué limitación encuentras en el algoritmo?
El código permite agregar obstáculos adicionales (por ejemplo, celdas con 'M' o 'W' que tienen un costo alto). Una limitación es que, en laberintos muy grandes o con muchos obstáculos, el consumo de memoria y tiempo de cómputo puede crecer rápidamente, ya que A* explora muchos nodos. Además, si los costos no están bien definidos (por ejemplo, si hay ciclos de bajo costo), el algoritmo puede tardar más en encontrar la solución óptima