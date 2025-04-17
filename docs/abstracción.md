# Índice de Replicación de Código (Frakes & Terry)

Se utiliza la fórmula Frakes & Terry propuesta por Isaac. El nivel de abstracción son las "líneas de código" con los siguientes niveles de reutilización:

- External Reuse Level (ERL):
ERL = E / L
- Internal Reuse Level (IRL):
IRL = M / L
- Total Reuse Level (TRL):
TRL = ERL + IRL

Donde:

- L = el número total de lower level items (en este caso el total de líneas de código LOC)
- E: el total de items de repositorios externos (librerías o módulos)
- M: el número total de items no externos que son usados más de una vez (funciones y métodos)

Esta fórmula no se ha automatizado. Sin embargo, con las librerías utilizadas hasta el momento (ast, tokenize, etc), se sabe que es posible hacerlo.

# Complejidad Ciclomática
Para la complejidad ciclomática se utiliza la librería Radon. Anteriormente, se hacía un promedio con la cantidad de items (funciones y métodos) tomados en cuenta. Tras lo discutido en reuniones, ahora se tomará en cuenta el total obtenido en vez del promedio.

# Tamaño promedio de función o método
Para este caso dividimos la cantidad de líneas de código entre el número de funciones. Ambos son datos sacados de la librería Radon con su módulo "metrics".

# Índice de Duplicación de Código
Aún está en proceso. Se ha intentado obtener con Sonarqube y Pylint (pylint --disable=all --enable=duplicate-code tu_archivo.py). El algoritmo Rabin-Karp programado aún no está completo y debe vincularse a un AST para poder ser más preciso. De momento el algoritmo es el siguiente:

1. Se eliminan comentarios y espacios extra.

2. Se preservan los saltos de línea.

3. Se analizan fragmentos de código con diferentes longitudes.

4. Se comparan fragmentos en distintas posiciones del código.

5. Se evita reportar duplicados ya detectados.

Este algoritmo funciona en texto plano, por lo que no es del todo preciso. La idea es que con el AST se establezca un hash para las tokens y a partir de ese hash establecer si hay similitudes o no.