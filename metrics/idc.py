import sys
import argparse

def normalize_code(code):
    """
    Normaliza el código eliminando espacios extra y comentarios.
    Mantiene los saltos de línea para mejor legibilidad.
    """
    lines = []
    for line in code.split('\n'):
        # Eliminar comentarios y espacios extra
        line = line.split('#')[0].strip()
        if line:
            lines.append(line)
    return '\n'.join(lines)

def find_duplicates(code, min_length=30):
    """
    Encuentra fragmentos de código duplicados.
    
    Args:
        code (str): Código fuente a analizar
        min_length (int): Longitud mínima para considerar un duplicado
    
    Returns:
        list: Lista de duplicados encontrados (texto, línea_inicio1, línea_inicio2)
    """
    code = normalize_code(code)
    lines = code.split('\n')
    duplicates = []
    
    # Para cada posible longitud de fragmento (en líneas)
    for window_size in range(1, len(lines) // 2 + 1):
        # Para cada posición inicial posible
        for i in range(len(lines) - window_size + 1):
            fragment1 = '\n'.join(lines[i:i + window_size])
            if len(fragment1) < min_length:
                continue
                
            # Buscar este fragmento en el resto del código
            for j in range(i + window_size, len(lines) - window_size + 1):
                fragment2 = '\n'.join(lines[j:j + window_size])
                if fragment1 == fragment2:
                    # Evitar duplicados ya reportados
                    duplicate_entry = (fragment1, i, j)
                    if not any(d[0] == fragment1 for d in duplicates):
                        duplicates.append(duplicate_entry)
    
    return duplicates

def format_duplicates_report(code, duplicates):
    """
    Genera un reporte formateado de los duplicados encontrados.
    """
    if not duplicates:
        return "No se encontraron duplicados significativos."
    
    lines = code.split('\n')
    report = []
    report.append("=== REPORTE DE CÓDIGO DUPLICADO ===\n")
    
    for duplicate_code, start1, start2 in duplicates:
        report.append(f"Código duplicado encontrado:")
        report.append(f"Primera ocurrencia (línea {start1 + 1}):")
        report.append("```")
        report.append(duplicate_code)
        report.append("```")
        report.append(f"\nSegunda ocurrencia (línea {start2 + 1}):")
        report.append("```")
        report.append(duplicate_code)
        report.append("```")
        report.append("-" * 50 + "\n")
    
    return "\n".join(report)

def analyze_file(file_path, min_length=30):
    """
    Analiza un archivo en busca de código duplicado.
    
    Args:
        file_path (str): Ruta al archivo a analizar
        min_length (int): Longitud mínima para considerar un duplicado
    
    Returns:
        str: Reporte de duplicados encontrados
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            code = file.read()
        duplicates = find_duplicates(code, min_length)
        return format_duplicates_report(code, duplicates)
    except FileNotFoundError:
        return f"Error: No se encontró el archivo '{file_path}'"
    except Exception as e:
        return f"Error al procesar el archivo: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description='Detector de código duplicado')
    parser.add_argument('file', help='Archivo a analizar')
    parser.add_argument('--min-length', type=int, default=30,
                      help='Longitud mínima para considerar un duplicado (default: 30)')
    
    args = parser.parse_args()
    print(analyze_file(args.file, args.min_length))

if __name__ == "__main__":
    main()