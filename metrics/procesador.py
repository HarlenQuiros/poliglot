import radon.raw as raw
import radon.complexity as complexity
import radon.metrics as metrics
import sys
import os

def analyze_code(file_path):
    with open(file_path, 'r') as file:
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


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Use: python procesador.py <file_path_or_dir_path>")
        sys.exit(1)

    path = sys.argv[1]
    if os.path.isfile(path):
        analyze_code(path)
    elif os.path.isdir(path):
        analyze_directory(path)
    else:
        print(f"Ruta no válida: {path}")
        sys.exit(1)
