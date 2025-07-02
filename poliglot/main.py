import argparse
from .upload.drive import get_groups, get_exercises, get_drive
from .metrics.radon import run_radon_metrics
from .metrics.inn import run_inn_metrics
from poliglot.metrics.coherence import run_coherence_metrics
from poliglot.metrics.idc import analyze_file as run_idc_metrics
from poliglot.metrics.irc import analyze_file as run_irc_metrics
from poliglot.utils.extract_python_files import save_python_files_from_excel

def drive_group(path, drive):
    get_groups(path + "grupos.xlsx", drive) # Assume the standarized file name

def drive_exercises(path, drive):
    get_exercises(path, drive)

def main():
    parser = argparse.ArgumentParser(description='Welcome to Poliglot')

    # Options
    parser.add_argument('-dg', '--drive_group', type=str,
                        help='Download groups from drive path and upload them to DB.\nThe path must be "DATOS/year-semester/".')
    parser.add_argument('-de', '--drive_exercises', type=str,
                        help='Download exercises from drive path and upload them to DB.\nThe path must be "DATOS/year-semester/professor full name".')
    parser.add_argument('-m', '--metrics', type=str,
                        help='Analyze code metrics (radon), identifier case metrics (inn), and semantic similarity (sustEj) for a file or directory. Output is written to output.txt in the project root.')
    # Remove -s/--statement, and make -epf only require excel path
    parser.add_argument('-epf', '--extract_python_files', type=str, metavar='EXCEL_PATH',
                        help='Extract python files from an Excel file. Usage: -epf <excel_path>')

    args = parser.parse_args()

    # Cases
    if args.drive_group:
        drive = get_drive()
        drive_group(args.drive_group, drive)
    if args.drive_exercises:
        drive = get_drive()
        drive_exercises(args.drive_exercises, drive)
    if args.metrics:
        metric_args = args.metrics.split()
        metric_path = metric_args[0]
        statement_path = metric_args[1] if len(metric_args) > 1 else None
        analyze_and_write_metrics(metric_path, statement_path)
    if args.extract_python_files:
        excel_path = args.extract_python_files
        save_python_files_from_excel(excel_path, './codes')
        print(f"Archivos generados exitosamente.")

def analyze_and_write_metrics(metric_path, statement_path=None):
    import os
    results = []
    def get_py_files(path):
        if os.path.isfile(path) and path.endswith('.py'):
            return [path]
        py_files = []
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith('.py'):
                    py_files.append(os.path.join(root, file))
        return py_files

    py_files = get_py_files(metric_path)
    if not py_files:
        results.append(f"No Python files found in {metric_path}")
    sustej_results = None
    if statement_path:
        sustej_results = run_coherence_metrics(metric_path, statement_path)  # dict: {filepath: result}
    for file in py_files:
        results.append(f"=== FILE: {file} ===")
        results.append("--- RADON METRICS ---")
        results.append(run_radon_metrics(file))
        results.append("--- INN METRICS ---")
        results.append(run_inn_metrics(file))
        results.append("--- IDC METRICS ---")
        results.append(run_idc_metrics(file))
        results.append("--- IRC METRICS ---")
        results.append(run_irc_metrics(file))
        if statement_path and sustej_results and file in sustej_results:
            results.append("--- COHERENCE METRICS ---")
            results.append(sustej_results[file])
        results.append("")
    with open('output.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(results))
    print('Radon, INN, and SustEj metrics written to output.txt, grouped by file.')

if __name__ == '__main__':
    main()
