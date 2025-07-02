import ast
import os
from collections import Counter, defaultdict

def run_irc_metrics(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        codigo = file.readlines()

    # L: contar líneas útiles (no vacías ni comentarios)
    lineas_utiles = [
        linea for linea in codigo
        if linea.strip() and not linea.strip().startswith("#")
    ]
    L = len(lineas_utiles)

    # Parsear AST
    with open(filepath, 'r', encoding='utf-8') as f:
        tree = ast.parse(f.read(), filename=filepath)

    imports_externos = set()
    funciones_definidas = set()
    llamadas_funciones = []
    modulos_importados = set()

    class Analizador(ast.NodeVisitor):
        def visit_Import(self, node):
            for alias in node.names:
                modulos_importados.add(alias.name.split('.')[0])
            imports_externos.add(node.lineno)
            self.generic_visit(node)

        def visit_ImportFrom(self, node):
            if node.module:
                modulos_importados.add(node.module.split('.')[0])
            imports_externos.add(node.lineno)
            self.generic_visit(node)

        def visit_FunctionDef(self, node):
            funciones_definidas.add(node.name)
            self.generic_visit(node)

        def visit_Call(self, node):
            if isinstance(node.func, ast.Attribute):
                if isinstance(node.func.value, ast.Name):
                    modulo = node.func.value.id
                    if modulo in modulos_importados:
                        llamadas_funciones.append((f"{modulo}.{node.func.attr}", node.lineno))
            elif isinstance(node.func, ast.Name):
                llamadas_funciones.append((node.func.id, node.lineno))
            self.generic_visit(node)

    Analizador().visit(tree)

    # E: contar líneas de llamadas a funciones de módulos importados
    lineas_uso_externo = set(imports_externos)
    for nombre, lineno in llamadas_funciones:
        if "." in nombre:  # indica que es del tipo modulo.funcion
            lineas_uso_externo.add(lineno)
    E = len(lineas_uso_externo)

    # M: contar funciones internas usadas más de una vez
    contador_llamadas = Counter(nombre for nombre, _ in llamadas_funciones)
    lineas_uso_interno = set()
    for funcion in funciones_definidas:
        if contador_llamadas[funcion] > 1:
            for nombre, lineno in llamadas_funciones:
                if nombre == funcion:
                    lineas_uso_interno.add(lineno)
    M = len(lineas_uso_interno)

    # Cálculos
    ERL = E / L if L else 0
    IRL = M / L if L else 0
    TRL = ERL + IRL

    # Formato de reporte tipo string
    report = []
    report.append(f"Archivo: {os.path.basename(filepath)}")
    report.append(f"L (líneas útiles): {L}")
    report.append(f"E (líneas uso externo): {E}")
    report.append(f"M (líneas uso interno): {M}")
    report.append(f"ERL (External reuse/L): {round(ERL, 4)}")
    report.append(f"IRL (Internal reuse/L): {round(IRL, 4)}")
    report.append(f"TRL (Total reuse/L): {round(TRL, 4)}")
    return '\n'.join(report)


# Para compatibilidad con el main
def analyze_file(file_path: str, min_length: int = 3) -> str:
    try:
        return run_irc_metrics(file_path)
    except FileNotFoundError:
        return f"Error: No se encontró el archivo '{file_path}'"
    except Exception as e:
        return f"Error al procesar el archivo: {str(e)}"


# CLI opcional para uso directo
if __name__ == "__main__":
    import sys
    import glob
    entradas = sys.argv[1:]
    archivos = []
    for entrada in entradas:
        archivos.extend(glob.glob(entrada))
    for archivo in archivos:
        print(run_irc_metrics(archivo))
        print()

