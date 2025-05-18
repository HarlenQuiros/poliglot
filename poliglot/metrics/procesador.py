import radon.raw as raw
import radon.complexity as complexity
import radon.metrics as metrics
import sys
import os
import ast
import re
from collections import Counter
import builtins
import argparse

builtin_names = dir(builtins)

def analyze_code(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        source_code = file.read()

    # Raw Metrics
    raw_metrics = raw.analyze(source_code)
    print("Raw Metrics:")
    print(f"Lines of Code (LOC): {raw_metrics.loc}")
    print(f"Logical Lines of Code (LLOC): {raw_metrics.lloc}")
    print(f"Source Lines of Code (SLOC): {raw_metrics.sloc}")
    print(f"Comments: {raw_metrics.comments}")
    print(f"Multi: {raw_metrics.multi}")
    print(f"Blank: {raw_metrics.blank}")
    print()

    # Cyclomatic Complexity
    cc_result = complexity.cc_visit(source_code)
    total_complexity = sum([block.complexity for block in cc_result])
    mean_complexity = total_complexity / len(cc_result)
    print(f"Average Complexity: {mean_complexity}")
    print(f"Total Complexity: {total_complexity}")
    print(f"Max Complexity: {max([block.complexity for block in cc_result])}")
    print(f"Min Complexity: {min([block.complexity for block in cc_result])}")
    print(f"Amount of Functions: {len(cc_result)}")
    print("Cyclomatic Complexity Metrics:")
    for block in cc_result:
        print(f"Function {block.name} - Complexity: {block.complexity}")
    print()

    # Maintainability Index
    mi = metrics.mi_visit(source_code, True)
    print(f"Maintainability Index: {mi}")
    print()

    # General halstead
    halstead_results = metrics.h_visit(source_code)
    print("General Halstead Metrics:")
    print_halstead(halstead_results[0])
    print("Halstead Metrics per Function")
    for f in halstead_results[1]:
        print(f"  Function: {f[0]}")
        print_halstead(f[1])


def print_halstead(h):
    print(f"  h1 (distinct operators): {h.h1}")
    print(f"  h2 (distinct operands): {h.h2}")
    print(f"  N1 (total operators): {h.N1}")
    print(f"  N2 (total operands): {h.N2}")
    print(f"  Vocabulary: {h.vocabulary}")
    print(f"  Length: {h.length}")
    print(f"  Calculated Length: {h.calculated_length}")
    print(f"  Volume: {h.volume}")
    print(f"  Difficulty: {h.difficulty}")
    print(f"  Effort: {h.effort}")
    print(f"  Time: {h.time}")
    print(f"  Bugs: {h.bugs}")
    print()


def analyze_directory(directory_path):
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                print(f"File: {file}")
                analyze_code(file_path)


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
        print(identifier)
        case_counts['PascalCase'] += 1
    elif kebab_case.match(identifier):
        case_counts['kebab-case'] += 1
    else:
        case_counts['unknown'] += 1


def analyze_code_case_frequency(code):
    tree = ast.parse(code)
    identifiers = set()
    
    # Go through the AST nodes and collect all identifiers
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.ClassDef):
            if node.name not in builtin_names and not (node.name.startswith('__') and node.name.endswith('__')):  # Avoid built-in names
                identifiers.add(node.name)

        elif isinstance(node, ast.Name):
            if node.id not in builtin_names and not (node.id.startswith('__') and node.id.endswith('__')):  # Avoid built-in names
                identifiers.add(node.id)

    # Classify the case of each identifier
    case_counts = Counter()
    
    for identifier in identifiers:
        classify_case(identifier, case_counts)
    # Determine the dominant case
    total_identifiers = sum(case_counts.values())
    if total_identifiers == 0:
        return "No identifiers found"
    
    dominant_case = case_counts.most_common(1)[0]
    dominant_case_count = dominant_case[1]
    
    # Calculate the proportion of the dominant case
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

    print(f"Total de identificadores: {result['total_identifiers']}")
    print(f"Estilo dominante: {result['dominant_case']}")
    print(f"Proporción del estilo dominante: {result['proportion']:.2%}")
    print("Conteo de estilos:", result['case_counts'])


def analyze_directory_inn(directory_path):
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                print(f"File: {file}")
                analyze_code_inn(file_path)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Welcome to Poliglot')
    
    # Options
    parser.add_argument('-r', '--radon', type=str, 
                        help='Get the radon metrics(cc, halstead, ...) of a dir or file.')
    parser.add_argument('-inn', '--inn', type=str, 
                        help='Get the case frequency(Herson\'s metrics) of the identifiers in a dir or file.')
    
    args = parser.parse_args()

    if args.radon:
        path = args.radon
        if os.path.isfile(path):
            analyze_code(path)
        elif os.path.isdir(path):
            analyze_directory(path)
        else:
            print(f"Invalid path: {path}")
            sys.exit(1)
    elif args.inn:
        path = args.inn
        if os.path.isfile(path):
            analyze_code_inn(path)
        elif os.path.isdir(path):
            analyze_directory_inn(path)
        else:
            print(f"Invalid path: {path}")
            sys.exit(1)

