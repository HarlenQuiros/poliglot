# Poliglot: Documentación del Proceso

Durante este proceso se ha realizado una serie de actividades con el fin de analizar ciertas métricas asociadas con el pensamiento computacional en evaluaciones aplicadas en los cursos de 'Introduccion a la programación' y 'Taller de programación' en estudiantes del Tecnológico de costa rica (TEC). El objetivo principal es identificar una manera viable de automatizar el proceso de evaluación de los estudiantes, esto mediante un análisis de los datos obtenidos a lo largo del proceso.

## Actividades Realizadas
Primeramente se realizó un análisis manual de los datos provistos por los profesores, esto con el fin de identificar patrones en los datos y así poder identificar una forma de automatizar el proceso de evaluación. Se fueron identificando diversas herramientas como Radon, SonarQube, Pylint, entre otras; las cuales se fueron probando para evaluar su desempeño en la definición de métricas. Algunas de estas herramientas fueron conservadas, otras reemplazadas por otras más eficientes y cómodas para poder automatizar.

Recientemente se realizó una actividad programada de manera presencial, donde los estudiantes tuvieron que realizar una serie de ejercicios previamente seleccionados con el fin de evaluar distintas capacidades asociadas con el pensamiento computacional y las métricas seleccionadas para la investigación. Con base en los resultados obtenidos en esta actividad se realizó un análisis de las métricas por iteraciones, seleccionando cierta cantidad de ejercicios para cada iteración (de distintas calidades según un análisis experto previo).

## Herramientas y Métricas Empleadas
El análisis del código fuente se desarrolló mediante una combinación de herramientas propias y bibliotecas especializadas de análisis estático. Estas herramientas permitieron extraer un conjunto amplio de métricas que abarcan complejidad, nomenclatura, estilo, coherencia, reutilización estructural y alineación con el enunciado del problema. 

Muchas de estas herramientas se llegaron a implementar luego de varias iteraciones manuales y revisiones exhaustivas del funcionamiento. Algunas herramientas fueron descartadas pues no mostraban un impacto relevante en la calificación obtenida, como por ejemplo SonarQube, Pylint y otras.Estas iteraciones se dieron gracias a los datos recopilados durante el 2024. Estos datos fueron migrados desde un Google Drive a un deploy de una base de datos MySQL en Railway. 

A continuación, se detalla cómo se implementó cada parte del análisis.

### 1. Radon (Complejidad, Mantenibilidad y Métricas Halstead)
Se utilizó la biblioteca Radon para obtener métricas fundamentales del código:

- Líneas de código, Comentarios, número de funciones y complejidad ciclomática.

- Complejidad ciclomática (CC): Para medir el número de caminos independientes posibles en el flujo de ejecución.

- Estas métricas se agruparon bajo los campos: LoCode, LoComments, NoFunctions, ERL, IRL, IRC, CC, TPFM, IDC.


### 2. Detector de Duplicación Estructural (AST y NodeVisitor)
Se desarrolló un analizador personalizado basado en el módulo ast de Python para detectar duplicación estructural significativa. Este analizador genera secuencias estructurales ignorando los valores concretos y utilizando una ventana deslizante para encontrar repeticiones no triviales.

- Patrones repetidos en estructura.

- Porcentaje de duplicación respecto a líneas significativas (IDC).

- Estos datos permitieron construir métricas como Valor general 2 y Nivel de PA (pensamiento algorítmico).

### 3. Análisis de Estilo de Identificadores (INN)
Se desarrolló un módulo que clasifica los identificadores (variables, funciones, clases) en diferentes estilos de nomenclatura: snake_case, camelCase, PascalCase, kebab-case. Se identificó el estilo dominante (INN) y su proporción de uso.

- Esto se interpretó como una métrica indirecta de coherencia en la nomenclatura y  a buenas prácticas de codificación.

### 4. Coherencia Semántica con el Enunciado (Jaccard Similarity)
Se implementó un análisis de similitud entre el enunciado traducido (usando deep-translator) y:

- Las variables definidas en el código.

- Los comentarios encontrados mediante expresiones regulares.

Estas palabras se tradujeron y lematizaron con NLTK y Stanza, y luego se calculó la similitud de Jaccard con las palabras clave extraídas del enunciado (ICLC, Comentarios).

El objetivo fue evaluar si el estudiante modeló correctamente los conceptos del problema dentro del código.

## Limpieza de Datos
En cuanto a la limpieza de datos, este proceso se llevó a cabo de manera manual principalmente, ya que se trataba de un conjunto de datos pequeño, aunque lo ideal sería buscar una manera de automatizar este proceso para un conjunto de datos más grande. Al tratarse de un conjunto de datos obtenidos de estudiantes de primer ingreso, ciertas soluciones se encontraban incompletas, con errores (sintácticos, lógicos, excepciones, etc.) o inclusive no se recibía la solución de cierto ejercicio. Por lo tanto, los estudiantes asistentes filtraron los datos con el fin de eliminar aquellas soluciones que no proveerían un insight importante para el análisis.

## Resultados Obtenidos
### Ejercicio 1

Para el primer ejercicio, se recopilaron las siguientes métricas principales:

| Métrica | Valor Mínimo | Valor Máximo | Promedio | Desviación Estándar |
|---------|--------------|--------------|----------|---------------------|
| Complejidad Ciclomática (CC) | 1 | 10 | 3.5 | 1.7 |
| Tamaño Promedio por Función (TPFM) | 1.7 | 41 | 12.1 | 8.6 |
| Duplicación de Código (IDC) | 0 | 0.67 | 0.29 | 0.21 |
| Líneas de Código (LoCode) | 2 | 50 | 15.3 | 10.9 |

Según los datos, este ejercicio mostró una distribución variada de calificaciones, con un 45% de soluciones clasificadas como "Buenas", un 35% como "Malas" y un 20% como "Regulares". Las soluciones con mejor clasificación generalmente presentaron valores de complejidad ciclomática moderados (entre 2 y 4) y un tamaño promedio por función más reducido.

### Ejercicio 2

Los resultados para el segundo ejercicio mostraron:

| Métrica | Valor Mínimo | Valor Máximo | Promedio | Desviación Estándar |
|---------|--------------|--------------|----------|---------------------|
| Complejidad Ciclomática (CC) | 1 | 12 | 6.8 | 2.9 |
| Tamaño Promedio por Función (TPFM) | 5.5 | 28 | 15.1 | 6.5 |
| Duplicación de Código (IDC) | 0.15 | 0.78 | 0.39 | 0.17 |
| Líneas de Código (LoCode) | 11 | 30 | 21.1 | 8.3 |

Según los datos obtenidos, este ejercicio presentó un mayor desafío, con solo un 25% de soluciones clasificadas como "Buenas", un 60% como "Malas" y un 15% como "Regulares". Se observó un aumento significativo en la complejidad ciclomática y en el tamaño promedio de las funciones, así como en la duplicación de código, lo que refleja la mayor dificultad del problema planteado.

### Ejercicio 3

El tercer ejercicio presentó los siguientes resultados:

| Métrica | Valor Mínimo | Valor Máximo | Promedio | Desviación Estándar |
|---------|--------------|--------------|----------|---------------------|
| Complejidad Ciclomática (CC) | 3 | 14 | 7.9 | 3.7 |
| Tamaño Promedio por Función (TPFM) | 6 | 41 | 22.3 | 10.5 |
| Duplicación de Código (IDC) | 0 | 0.77 | 0.45 | 0.19 |
| Líneas de Código (LoCode) | 6 | 51 | 25.4 | 11.8 |

Este ejercicio mostró un 40% de soluciones clasificadas como "Buenas", un 45% como "Malas" y un 15% como "Regulares". Este ejercicio, que requería un mayor nivel de abstracción y manejo de estructuras de datos, mostró los valores más altos de complejidad y duplicación entre todos los ejercicios analizados.

### Ejercicio 4

Para el cuarto ejercicio, los resultados fueron:

| Métrica | Valor Mínimo | Valor Máximo | Promedio | Desviación Estándar |
|---------|--------------|--------------|----------|---------------------|
| Complejidad Ciclomática (CC) | 0 | 16 | 5.7 | 3.5 |
| Tamaño Promedio por Función (TPFM) | 4 | 38 | 15.7 | 8.9 |
| Duplicación de Código (IDC) | 0 | 0.74 | 0.33 | 0.15 |
| Líneas de Código (LoCode) | 4 | 51 | 20.8 | 11.5 |

Finalmente, este ejercicio presentó un 20% de soluciones clasificadas como "Buenas", un 70% como "Malas" y un 10% como "Regulares". A pesar de ser el último ejercicio, mostró valores de complejidad ciclomática ligeramente inferiores al ejercicio 3, posiblemente debido a que muchas soluciones quedaron incompletas o no funcionaban correctamente.

## Análisis de Resultados
### Ejercicio 1

1. **Relación con calificaciones**: Se observó una correlación moderada negativa (r ≈ -0.52) entre el valor general (que combina CC, TPFM e IDC) y la calidad de la solución. Las soluciones clasificadas como "Buenas" tendían a tener valores generales más bajos (promedio de 8.2) que las "Malas" (promedio de 13.5).

2. **Nivel de abstracción**: Las soluciones con nivel de abstracción "Alto" (valor > 0.8) recibieron mayoritariamente clasificaciones "Buenas", mientras que las de nivel "Bajo" (valor < 0.4) fueron generalmente clasificadas como "Malas".

3. **Pensamiento algorítmico**: El valor general 2, que refleja aspectos del pensamiento algorítmico, mostró una correlación positiva (r ≈ 0.61) con la calidad de la solución. Las soluciones "Buenas" presentaron un promedio de 0.48 en esta métrica, frente a 0.36 en las "Malas".

4. **Patrones de solución**: Las soluciones mejor calificadas se caracterizaban por:
   - Complejidad ciclomática moderada (2-4)
   - Tamaño promedio por función reducido (5-10 líneas)
   - Baja duplicación de código (<20%)
   - Buena coherencia en nomenclatura

### Ejercicio 2o:

1. **Impacto de la complejidad**: A diferencia del ejercicio 1, se encontró una correlación positiva (r ≈ 0.48) entre la complejidad ciclomática y la calidad de la solución. Esto sugiere que este ejercicio requería soluciones más elaboradas para ser efectivas.

2. **Recursividad**: Las soluciones que implementaron recursividad (indicado por valores más altos de IRL e IRC) obtuvieron mejores clasificaciones. El 80% de las soluciones "Buenas" utilizaron algún grado de recursividad.

3. **Nivel de pensamiento algorítmico**: Las soluciones con nivel de pensamiento algorítmico "Alto" fueron más frecuentes entre las clasificadas como "Buenas" (70%) que entre las "Malas" (30%).

4. **Tamaño de funciones**: A diferencia del ejercicio 1, las soluciones con funciones más pequeñas (TPFM < 10) tendieron a recibir mejores clasificaciones, lo que sugiere que la modularidad fue especialmente valorada en este ejercicio.

### Ejercicio 3

1. **Complejidad óptima**: Se identificó un rango óptimo de complejidad ciclomática (6-10) para este ejercicio. Las soluciones con CC fuera de este rango tendían a recibir peores clasificaciones.

2. **Impacto de la duplicación**: La duplicación de código mostró una fuerte correlación negativa (r ≈ -0.67) con la calidad de la solución. Las soluciones "Buenas" presentaron un promedio de IDC de 0.32, frente a 0.58 en las "Malas".

3. **Tamaño del código**: Contrariamente a lo esperado, no se encontró una correlación significativa entre el número de líneas de código y la calidad de la solución. Tanto soluciones extensas como concisas recibieron buenas clasificaciones si implementaban correctamente la funcionalidad requerida.

4. **Nivel de pensamiento algorítmico**: El 85% de las soluciones clasificadas como "Buenas" presentaron un nivel de pensamiento algorítmico "Medio" o "Alto", frente a solo un 40% de las "Malas".

### Ejercicio 4

Para el cuarto ejercicio:

1. **Completitud como factor clave**: La principal diferencia entre soluciones "Buenas" y "Malas" fue la completitud. El 75% de las soluciones clasificadas como "Malas" fueron marcadas como "No completado" o "No ejecuta".

2. **Eficiencia algorítmica**: Entre las soluciones completas, aquellas que implementaban algoritmos más eficientes (reflejado en menor CC y TPFM para la misma funcionalidad) recibieron mejores clasificaciones.

3. **Nivel de abstracción**: Las soluciones con nivel de abstracción "Alto" fueron más frecuentes entre las clasificadas como "Buenas" (60%) que entre las "Malas" (25%).

4. **Representación de datos**: A diferencia de los ejercicios anteriores, el nivel de representación de datos (INN) mostró variabilidad, con algunas soluciones clasificadas como "Buenas" presentando valores "Bajos" en esta métrica.

## Conclusiones
1. El análisis de los cuatro ejercicios demuestra que la relevancia y el peso de las diferentes métricas varía según el tipo y la complejidad del problema.

2. Las métricas analizadas (especialmente CC, TPFM, IDC, nivel de abstracción y valor general 2) demostraron ser buenos indicadores de diferentes aspectos del pensamiento computacional, lo que respalda su uso en sistemas de evaluación automatizada.

3. Aunque las métricas analizadas capturan aspectos importantes de la calidad del código, algunos factores como la creatividad, la elegancia de las soluciones o la adaptabilidad a requisitos cambiantes son difíciles de cuantificar. Por tanto, un sistema automatizado debería complementarse con evaluaciones cualitativas para ciertos aspectos del pensamiento computacional.

4. Los resultados respaldan el desarrollo de un modelo de evaluación que asigne diferentes pesos a las métricas según el tipo de ejercicio, considerando factores como la complejidad inherente del problema, el tiempo disponible y los objetivos específicos.
