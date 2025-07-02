import radon.raw as raw
import radon.complexity as complexity
import radon.metrics as metrics
import os

def analyze_code(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        source_code = file.read()

    output = []
    # Raw Metrics
    raw_metrics = raw.analyze(source_code)
    output.append("Raw Metrics:")
    output.append(f"Lines of Code (LOC): {raw_metrics.loc}")
    output.append(f"Logical Lines of Code (LLOC): {raw_metrics.lloc}")
    output.append(f"Source Lines of Code (SLOC): {raw_metrics.sloc}")
    output.append(f"Comments: {raw_metrics.comments}")
    output.append(f"Multi: {raw_metrics.multi}")
    output.append(f"Blank: {raw_metrics.blank}")

    # Cyclomatic Complexity
    cc_result = complexity.cc_visit(source_code)
    if cc_result:
        total_complexity = sum([block.complexity for block in cc_result])
        mean_complexity = total_complexity / len(cc_result)
        output.append(f"Average Complexity: {mean_complexity}")
        output.append(f"Total Complexity: {total_complexity}")
        output.append(f"Amount of Functions: {len(cc_result)}")
        output.append("")
    else:
        output.append("No functions found for cyclomatic complexity analysis.")
        output.append("")
    return '\n'.join(output)

def analyze_directory(directory_path):
    output = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                output.append(f"File: {file}")
                output.append(analyze_code(file_path))
                output.append("")
    return '\n'.join(output)

def run_radon_metrics(path):
    if os.path.isfile(path):
        return analyze_code(path)
    elif os.path.isdir(path):
        return analyze_directory(path)
    else:
        return f"Invalid path: {path}"
