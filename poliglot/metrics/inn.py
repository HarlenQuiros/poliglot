import os
import ast
import re
from collections import Counter
import builtins

builtin_names = dir(builtins)

def classify_case(identifier, case_counts):
    snake_case = re.compile(r'^[a-z0-9]+(_[a-z0-9]+)*$')
    camel_case = re.compile(r'^[a-z0-9]+([A-Z][a-z0-9]*)+$')
    pascal_case = re.compile(r'^[A-Z][a-z0-9]*([A-Z][a-z0-9]*)*$')
    kebab_case = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')

    if re.match(r'^[a-z][a-z0-9]*$', identifier):
        case_counts['snake_case'] += 1
        case_counts['kebab-case'] += 1
        case_counts['camelCase'] += 1
    elif snake_case.match(identifier):
        case_counts['snake_case'] += 1
    elif camel_case.match(identifier):
        case_counts['camelCase'] += 1
    elif pascal_case.match(identifier):
        case_counts['PascalCase'] += 1
    elif kebab_case.match(identifier):
        case_counts['kebab-case'] += 1
    else:
        case_counts['unknown'] += 1

def analyze_code_case_frequency(code):
    tree = ast.parse(code)
    identifiers = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.ClassDef):
            if node.name not in builtin_names and not (node.name.startswith('__') and node.name.endswith('__')):
                identifiers.add(node.name)
        elif isinstance(node, ast.Name):
            if node.id not in builtin_names and not (node.id.startswith('__') and node.id.endswith('__')):
                identifiers.add(node.id)
    case_counts = Counter()
    for identifier in identifiers:
        classify_case(identifier, case_counts)
    total_identifiers = sum(case_counts.values())
    if total_identifiers == 0:
        return "No identifiers found"
    dominant_case = case_counts.most_common(1)[0]
    dominant_case_count = dominant_case[1]
    proportion = dominant_case_count / len(identifiers)
    return {
        'total_identifiers': len(identifiers),
        'dominant_case': dominant_case[0],
        'dominant_case_count': dominant_case_count,
        'proportion': proportion,
        'case_counts': case_counts
    }

def analyze_code_inn(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        code = file.read()
    result = analyze_code_case_frequency(code)
    if isinstance(result, str):
        return result
    output = []
    output.append(f"Total de identificadores: {result['total_identifiers']}")
    output.append(f"Estilo dominante: {result['dominant_case']}")
    output.append(f"Proporción del estilo dominante: {result['proportion']:.2%}")
    output.append(f"Conteo de estilos: {dict(result['case_counts'])}")
    return '\n'.join(output)

def analyze_directory_inn(directory_path):
    output = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                output.append(f"File: {file}")
                output.append(analyze_code_inn(file_path))
                output.append("")
    return '\n'.join(output)

def run_inn_metrics(path):
    if os.path.isfile(path):
        return analyze_code_inn(path)
    elif os.path.isdir(path):
        return analyze_directory_inn(path)
    else:
        return f"Invalid path: {path}"
