# Poliglot

Poliglot es una plataforma para la gestión, análisis y evaluación automatizada de ejercicios de programación en cursos universitarios, principalmente cursos de primer ingreso. Permite extraer, almacenar y analizar soluciones de estudiantes, calculando métricas relevantes para el pensamiento computacional y facilitando la investigación educativa.

## Características

- **Extracción automática** de soluciones de estudiantes desde archivos Excel y Google Drive.
- **Carga y gestión** de datos en una base de datos MySQL mediante procedimientos almacenados.
- **Análisis de métricas** de código fuente usando herramientas como Radon y algoritmos personalizados:
  - Complejidad ciclomática
  - Tamaño promedio de función
  - Índice de duplicación de código (IDC)
  - Estilo de nomenclatura de identificadores
  - Métricas Halstead
- **Procesamiento de archivos PDF y CSV** para extraer enunciados y aspectos de ejercicios.
- **Documentación y reportes** para facilitar la investigación y el análisis de resultados.

## Estructura del Proyecto

- `poliglot/`  
  - `analyze/` — Módulos para analizar archivos Excel y PDF.
  - `codes/` — Directorios para almacenar soluciones de ejercicios.
  - `docs/` — Documentación del proceso, investigación y ejercicios anonimizados.
  - `metrics/` — Scripts para calcular métricas de código.
  - `stored_procedures/` — Procedimientos almacenados para la base de datos.
  - `upload/` — Scripts para interactuar con Google Drive.
  - `utils/` — Scrips varios para acceso a DB, requests a API útiles y extracción de soluciones desde un Excel.
  - `main.py` — Punto de entrada principal del sistema.

## Instalación

1. **Clona el repositorio**  
   ```sh
   git clone <url-del-repo>
   cd poliglot
   ```
2. **Instala las dependencias**
Se recomienda usar Poetry
   ```sh
   poetry install
   ```
3. **Configura las variables de entorno de ser necesario**
Las variables de entorno deben ser solicitadas para tener acceso a la BD en deploy.
4. **Configura Google Drive**
Coloca tu archivo `client_secrets.json` en la carpeta `poliglot/`

## Uso
Extraer y cargar grupos y ejercicios desde Google Drive
```sh
python .\poliglot\main.py -dg "DATOS/2024-1/"
python .\poliglot\main.py -de "DATOS/2024-1/Nombre Profesor/"
```

Extraer soluciones desde excel
```sh
python .\poliglot\utils\extract_python_files.py .\poliglot\actividadExcel.xlsx
```

Calcular métricas de código
```sh
python .\poliglot\metrics\procesador.py -r "folder or file"
python .\poliglot\metrics\procesador.py -inn "folder or file"
```

Analizar duplicación de código
```sh
python .\poliglot\metrics\idc.py -r "folder or file"
```

## Base de datos
El proyecto utiliza procedimientos almacenados para insertar y consultar datos. Los scripts SQL se encuentran en poliglot/stored_procedures/.

## Créditos
Desarrollado por el equipo de investigación de Pensamiento Computacional, TEC.