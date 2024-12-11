# Investigación de Algoritmos relacionados con el IDC

## Baker's algorithm
Consiste en un algoritmo de coincidencia de cadenas desarrollado por Brenda S. Baker en 1978. Es particularmente útil para detectar y ubicar fragmentos de código duplicado dentro de una base de código.

### ¿Cómo funciona?
El algoritmo funciona primero construyendo una representación de árbol de análisis normalizado del código. Luego compara estos árboles de análisis para identificar subárboles comunes, que corresponden a fragmentos de código duplicado. El algoritmo utiliza un enfoque basado en hash para comparar y hacer coincidir de manera eficiente los árboles de análisis.

### Ventajas
- Eficaz para detectar y ubicar fragmentos de código duplicado, incluso en presencia de cambios en el nombre de variables o cambios sintácticos menores.
- Eficiente, con una complejidad de tiempo de O(n log n), donde n es el tamaño de la base de código.
- Puede manejar bases de código grandes de manera efectiva.

### Limitaciones
- Requiere un analizador integral para construir los árboles de análisis normalizados, lo que puede ser complejo de implementar.
- Es posible que no sea tan efectivo para detectar código duplicado que se extiende a través de múltiples funciones o archivos.
- No siempre distingue entre la duplicación de código intencional y no intencional.

## Rabin–Karp string search algorithm
El algoritmo de búsqueda de cadenas Rabin-Karp es un algoritmo de coincidencia de cadenas que utiliza hash para buscar de manera eficiente un patrón dentro de un texto más grande.

### ¿Cómo funciona?
El algoritmo funciona calculando un valor hash para el patrón y el primer subcadena del texto con la misma longitud que el patrón. Luego desliza el patrón a través del texto, calculando un nuevo valor hash para cada subcadena y comparándolo con el valor hash del patrón. Si los valores hash coinciden, el algoritmo realiza una comparación carácter por carácter para verificar la coincidencia.

### Ventajas
- Eficiente, con una complejidad de tiempo promedio de O(n+m), donde n es la longitud del texto y m es la longitud del patrón.
- Se puede usar para buscar eficientemente múltiples patrones dentro de un texto más grande.
- Relativamente simple de implementar.

### Limitaciones
- Se basa en la suposición de que las colisiones de hash son poco frecuentes, lo cual puede no ser siempre el caso.
- Es posible que no sea tan efectivo para detectar código duplicado que implique cambios estructurales significativos o reorganizaciones.
- No proporciona información sobre la ubicación o la extensión de los fragmentos de código duplicado.

## Using abstract syntax trees
El uso de árboles de sintaxis abstracta (AST) es un enfoque común para detectar código duplicado en una base de código. Los AST proporcionan una representación estructurada de la sintaxis del código, que se puede analizar para identificar fragmentos de código similares.

### ¿Cómo funciona?
El proceso general implica los siguientes pasos:
1. Analizar la base de código para generar AST para cada archivo o función.
2. Recorrer los AST para extraer características o patrones relevantes.
3. Comparar las características o patrones extraídos para identificar similitudes y detectar fragmentos de código duplicado.

### Ventajas
- Proporciona una comprensión integral de la estructura y sintaxis del código.
- Puede detectar código duplicado incluso en presencia de cambios en el nombre de variables o cambios sintácticos menores.
- Puede identificar la ubicación y la extensión de los fragmentos de código duplicado.

### Limitaciones
- Requiere un analizador robusto y preciso para generar los AST, lo que puede ser complejo de implementar.
- Puede ser computacionalmente costoso, especialmente para bases de código grandes, debido a la complejidad de recorrer y comparar los AST.
- Es posible que no sea tan efectivo para detectar código duplicado que implique cambios estructurales significativos o reorganizaciones.
