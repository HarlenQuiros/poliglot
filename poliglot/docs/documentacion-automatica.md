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
