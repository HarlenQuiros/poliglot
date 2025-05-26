A continuación se detalla el procedimiento para analizar las métricas en los ejercicios realizados por los estudiantes en una actividad programada de manera presencial:
## Obtención de los datos
Se creó el script (python) `extract_python_files`, el cual se encarga de extraer los ejercicios las soluciones de los estudiantes a partir de un archivo excel. Así mismo, este script los organiza en carpetas (1, 2, 3, 4) según el mapeo definido:

| Grupo | Ejercicio | Etiqueta |
|-------|-----------|----------|
| A     | 1         | 1        |
| A     | 2         | 2        |
| A     | 3         | 3        |
| A     | 4         | 4        |
| B     | 1         | 1        |
| B     | 2         | 3        |
| B     | 3         | 4        |
| B     | 4         | 2        |
Cuando ya se tienen los archivos organizados en la carpeta `codes` y en las subcarpetas correspondientes se debe ejecutar otro script llamado `procesador.py`, el cual se encarga de calcular ciertas métricas mediante el uso de la biblioteca Radon. Entre las métricas calculadas se encuentran líneas de código, líneas de comentarios, complejidad ciclomática y cantidad de funciones.

Seguidamente se debe calcular de manera manual el ERL, IRL e IRC. Para esto se utiliza una fórmula basada en *Frakes, W., & Terry, C. (1996). Software reuse: metrics and models. ACM Computing Surveys (CSUR), 28(2), 415-435.* Para esto se debe calcular la cantidad de veces que se reutiliza un recurso externo y la cantidad de veces que se reutiliza un recurso interno. Finalmente, para el IRC se suman estos dos valores.

Para el cálculo del IDC es necesario ejecutar el script `idc.py`, el cual devuelve de manera automática el procentaje de código duplicado. Para finalizar las métricas de abstracción, el TPFM se calcula de manera semi-automática por medio de Excel, pues consiste en dividir la cantidad de líneas de código entre la cantidad de funciones.

Pasando a las métricas de Pensamiento Algorítmico se utiliza el script `sustEj.py`, el cual se encarga de traducir todo el código a inglés y aplicar el algoritmo *jaccard similarity* con el fin de identificar la similitud de nombres de variables y comentarios con el enunciado (traducido a inglés). Esto nos devuelve las métricas de Coherencia de nomenclatura y comentarios. Las métricas ICLC e ICC se calculan por medio de excel con sus respectivas fórmulas definidas.

Finalmente, para las métricas de Representación de Datos, el script  `procesador.py` puede ser ejecutado con la opción *--inn*  para que devuelva el valor correspondiente a esta métrica.

# Análisis de resultados
Los resultados del análisis de las cuatro actividades programadas revelan patrones interesantes sobre el desempeño estudiantil y la efectividad de las métricas de pensamiento computacional. A continuación se presenta un análisis detallado de cada ejercicio, destacando tanto las tendencias generales como los insights específicos encontrados.

## Ejercicio 1

### Métricas Generales
El primer ejercicio, diseñado como introducción a conceptos fundamentales, mostró la siguiente distribución de métricas:

| Métrica | Mínimo | Máximo | Promedio | Desv. Estándar |
|---------|--------|--------|----------|----------------|
| Complejidad Ciclomática (CC) | 1 | 10 | 3.5 | 1.7 |
| Tamaño Promedio por Función (TPFM) | 1.7 | 41 | 12.1 | 8.6 |
| Duplicación de Código (IDC) | 0 | 0.67 | 0.29 | 0.21 |
| Líneas de Código (LoCode) | 2 | 50 | 15.3 | 10.9 |

### Distribución de Calificaciones
- **Buenas**: 45% de las soluciones
- **Regulares**: 20% de las soluciones
- **Malas**: 35% de las soluciones

### Análisis Detallado

**Características de las Soluciones Exitosas:**
Las soluciones clasificadas como "Buenas" presentaron un patrón consistente: complejidad ciclomática moderada (entre 2-4), funciones concisas (5-10 líneas promedio) y mínima duplicación de código. Este patrón sugiere que los estudiantes exitosos aplicaron principios de programación limpia desde etapas tempranas.

**Desafíos Identificados:**
La alta variabilidad en el tamaño promedio por función (desviación estándar de 8.6) indica que algunos estudiantes aún no habían desarrollado criterios claros para la modularización del código. Las soluciones con TPFM superior a 25 líneas generalmente recibieron clasificaciones más bajas, sugiriendo problemas en la descomposición de problemas.

**Correlaciones Significativas:**
- Correlación negativa moderada (r ≈ -0.52) entre el valor general combinado y la calidad de la solución
- Las soluciones "Buenas" promediaron 8.2 en valor general, mientras que las "Malas" promediaron 13.5
- El nivel de abstracción mostró ser un predictor fuerte: soluciones con nivel "Alto" (>0.8) fueron mayoritariamente clasificadas como "Buenas"

## Ejercicio 2

### Métricas Generales

| Métrica | Mínimo | Máximo | Promedio | Desv. Estándar |
|---------|--------|--------|----------|----------------|
| Complejidad Ciclomática (CC) | 1 | 12 | 6.8 | 2.9 |
| Tamaño Promedio por Función (TPFM) | 5.5 | 28 | 15.1 | 6.5 |
| Duplicación de Código (IDC) | 0.15 | 0.78 | 0.39 | 0.17 |
| Líneas de Código (LoCode) | 11 | 30 | 21.1 | 8.3 |

### Distribución de Calificaciones
- **Buenas**: 25% de las soluciones
- **Regulares**: 15% de las soluciones
- **Malas**: 60% de las soluciones

### Análisis Detallado

**Aumento en la Dificultad:**
El ejercicio 2 representó un salto cualitativo significativo. El promedio de complejidad ciclomática casi se duplicó (de 3.5 a 6.8), y la duplicación de código aumentó considerablemente (de 0.29 a 0.39). Esto refleja que los estudiantes enfrentaron desafíos para mantener la calidad del código al abordar problemas más complejos.

**Patrones Contraintuitivos:**
Sorprendentemente, se encontró una correlación positiva (r ≈ 0.48) entre la complejidad ciclomática y la calidad de la solución. Esto sugiere que este ejercicio requería soluciones más elaboradas para ser efectivas, contrastando con el ejercicio 1 donde la simplicidad era valorada.

**Impacto de la Recursividad:**
El 80% de las soluciones "Buenas" implementaron algún grado de recursividad (valores altos de IRL e IRC), indicando que los estudiantes que dominaron conceptos avanzados obtuvieron mejores resultados. Esta métrica emergió como un diferenciador clave entre soluciones exitosas y fallidas.

**Modularización como Factor Crítico:**
Contrario al patrón general, las soluciones con funciones más pequeñas (TPFM < 10) tendieron a recibir mejores clasificaciones, sugiriendo que la modularización se volvió especialmente importante conforme aumentó la complejidad del problema.

## Ejercicio 3

### Métricas Generales

| Métrica | Mínimo | Máximo | Promedio | Desv. Estándar |
|---------|--------|--------|----------|----------------|
| Complejidad Ciclomática (CC) | 3 | 14 | 7.9 | 3.7 |
| Tamaño Promedio por Función (TPFM) | 6 | 41 | 22.3 | 10.5 |
| Duplicación de Código (IDC) | 0 | 0.77 | 0.45 | 0.19 |
| Líneas de Código (LoCode) | 6 | 51 | 25.4 | 11.8 |

### Distribución de Calificaciones
- **Buenas**: 40% de las soluciones
- **Regulares**: 15% de las soluciones
- **Malas**: 45% de las soluciones

### Análisis Detallado

**Complejidad Óptima Identificada:**
Este ejercicio reveló un hallazgo importante: existe un rango óptimo de complejidad ciclomática (6-10) para problemas de este nivel. Las soluciones que se salían de este rango, tanto por exceso como por defecto, tendían a recibir clasificaciones más bajas. Esto sugiere que la complejidad apropiada es específica del contexto del problema.

**Duplicación como Factor Crítico:**
La duplicación de código mostró la correlación negativa más fuerte observada (r ≈ -0.67) con la calidad de la solución. Las soluciones "Buenas" promediaron IDC de 0.32, mientras que las "Malas" alcanzaron 0.58. Esto indica que conforme aumenta la complejidad del problema, la capacidad de evitar duplicación se vuelve un indicador crucial de habilidad de programación.

**Paradoja del Tamaño:**
Contrariamente a las expectativas, no se encontró correlación significativa entre el número de líneas de código y la calidad de la solución. Tanto soluciones extensas como concisas recibieron buenas clasificaciones si implementaban correctamente la funcionalidad. Esto sugiere que la efectividad no está necesariamente relacionada con la brevedad del código.

**Pensamiento Algorítmico como Predictor:**
El 85% de las soluciones "Buenas" presentaron nivel de pensamiento algorítmico "Medio" o "Alto", frente a solo 40% de las "Malas". Esta métrica demostró ser uno de los predictores más confiables de éxito en problemas que requieren mayor abstracción.

## Ejercicio 4

### Métricas Generales

| Métrica | Mínimo | Máximo | Promedio | Desv. Estándar |
|---------|--------|--------|----------|----------------|
| Complejidad Ciclomática (CC) | 0 | 16 | 5.7 | 3.5 |
| Tamaño Promedio por Función (TPFM) | 4 | 38 | 15.7 | 8.9 |
| Duplicación de Código (IDC) | 0 | 0.74 | 0.33 | 0.15 |
| Líneas de Código (LoCode) | 4 | 51 | 20.8 | 11.5 |

### Distribución de Calificaciones
- **Buenas**: 20% de las soluciones
- **Regulares**: 10% de las soluciones
- **Malas**: 70% de las soluciones

### Análisis Detallado

**La Completitud como Factor Dominante:**
El ejercicio 4 reveló una realidad importante: la completitud se volvió el factor más determinante. El 75% de las soluciones clasificadas como "Malas" fueron marcadas como "No completado" o "No ejecuta". Esto sugiere que conforme aumenta la dificultad, la capacidad de terminar el ejercicio se convierte en el principal diferenciador.

**Paradoja de la Complejidad Reducida:**
Interesantemente, la complejidad ciclomática promedio (5.7) fue menor que la del ejercicio 3 (7.9), posiblemente debido a que muchas soluciones quedaron incompletas. Esto ilustra cómo las métricas pueden ser engañosas cuando se aplican a código incompleto.

**Eficiencia Algorítmica en Foco:**
Entre las soluciones completas, aquellas que implementaron algoritmos más eficientes (menor CC y TPFM para la misma funcionalidad) recibieron mejores clasificaciones. Esto indica que en niveles avanzados, la elegancia de la solución se vuelve más relevante.

**Variabilidad en Representación de Datos:**
A diferencia de ejercicios anteriores, el nivel de representación de datos (INN) mostró gran variabilidad, con algunas soluciones "Buenas" presentando valores "Bajos". Esto sugiere que en problemas complejos, diferentes enfoques de representación pueden ser igualmente válidos.

## Tendencias Transversales

### Evolución de la Dificultad
Los datos muestran una progresión clara en la dificultad:
- **Ejercicio 1**: Enfoque en fundamentos, alta tasa de éxito (65% buenas/regulares)
- **Ejercicio 2**: Introducción de complejidad, caída en el rendimiento (40% buenas/regulares)
- **Ejercicio 3**: Recuperación parcial con enfoque en abstracción (55% buenas/regulares)
- **Ejercicio 4**: Desafío máximo, tasa de éxito mínima (30% buenas/regulares)

### Métricas Más Predictivas por Ejercicio
- **Ejercicio 1**: Nivel de abstracción y valor general
- **Ejercicio 2**: Recursividad y modularización
- **Ejercicio 3**: Duplicación de código y pensamiento algorítmico
- **Ejercicio 4**: Completitud y eficiencia algorítmica

### Patrones de Aprendizaje Identificados
1. **Estudiantes Consistentes**: Mantuvieron calidad alta en todos los ejercicios (15% del total)
2. **Estudiantes en Desarrollo**: Mejoraron progresivamente hasta el ejercicio 3 (25% del total)
3. **Estudiantes con Dificultades**: Mostraron declive progresivo (35% del total)
4. **Estudiantes Inconsistentes**: Rendimiento variable sin patrón claro (25% del total)

## Implicaciones para la Evaluación Automatizada

Los resultados sugieren que un sistema de evaluación automatizada efectivo debe:

1. **Adaptar pesos de métricas según el tipo de ejercicio**: La relevancia de cada métrica varía significativamente entre ejercicios
2. **Considerar la completitud como prerrequisito**: En ejercicios complejos, la funcionalidad básica debe evaluarse antes que la elegancia
3. **Implementar umbrales dinámicos**: Los rangos óptimos de métricas cambian según la complejidad del problema
4. **Integrar múltiples indicadores**: Ninguna métrica individual es suficiente para evaluar pensamiento computacional
