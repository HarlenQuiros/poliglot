import sys
import argparse
import ast
from dataclasses import dataclass
from typing import List, Tuple, Set

@dataclass
class DuplicateInfo:
    structure: List[str]
    occurrences: List[Tuple[int, int]] 
    node_count: int

class StructuralDuplicateDetector(ast.NodeVisitor):
    def __init__(self):
        self.structure_sequences = []
        self.current_sequence = []
        self.line_mappings = {}
        self.total_lines = 0
        
    def visit(self, node):
        if hasattr(node, 'lineno'):
            start_line = node.lineno
            end_line = node.end_lineno if hasattr(node, 'end_lineno') else start_line
            
            structure = self._get_node_structure(node)
            if structure:
                self.current_sequence.append(structure)
                self.line_mappings[len(self.current_sequence) - 1] = (start_line, end_line)
        
        self.generic_visit(node)

    def _get_node_structure(self, node) -> str:
        """Extract structural information while ignoring specific values"""
        node_type = type(node).__name__
        
        if isinstance(node, ast.Name):
            return f"Name"
        elif isinstance(node, ast.Num):
            return f"Num"
        elif isinstance(node, ast.Str):
            return f"Str"
        elif isinstance(node, ast.Call):
            return f"Call"
        elif isinstance(node, ast.BinOp):
            return f"BinOp_{type(node.op).__name__}"
        elif isinstance(node, ast.Compare):
            return f"Compare_{[type(op).__name__ for op in node.ops]}"
        else:
            return node_type

    def _is_overlapping(self, range1: Tuple[int, int], range2: Tuple[int, int]) -> bool:
        """Check if two line ranges overlap"""
        start1, end1 = range1
        start2, end2 = range2
        return not (end1 < start2 or end2 < start1)

    def _filter_overlapping_duplicates(self, duplicates: List[DuplicateInfo]) -> List[DuplicateInfo]:
        """Filter out overlapping duplicates, keeping the larger ones"""
        # Sort duplicates by line count (descending) and then by start line
        duplicates.sort(key=lambda x: (-(x.occurrences[0][1] - x.occurrences[0][0]), x.occurrences[0][0]))
        
        filtered_duplicates = []
        used_lines: Set[int] = set()
        
        for dup in duplicates:
            # Check if this duplicate overlaps with any already used lines
            is_valid = True
            current_lines = set()
            
            for start, end in dup.occurrences:
                for line in range(start, end + 1):
                    if line in used_lines:
                        is_valid = False
                        break
                    current_lines.add(line)
                
                if not is_valid:
                    break
            
            if is_valid:
                filtered_duplicates.append(dup)
                used_lines.update(current_lines)
        
        return filtered_duplicates

    def _count_significant_lines(self, code: str) -> int:
        """Count significant lines (non-empty, non-comment) in the code"""
        lines = code.split('\n')
        count = 0
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and not (line.startswith('"""') and line.endswith('"""')):
                count += 1
        return count

    def analyze_code(self, code: str, min_length: int = 3) -> Tuple[List[DuplicateInfo], float]:
        """Analyze code and return duplicates along with duplication percentage"""
        tree = ast.parse(code)
        self.visit(tree)
        
        # Find duplicates using sliding window
        all_duplicates = []
        
        for window_size in range(min_length, len(self.current_sequence) + 1):
            for i in range(len(self.current_sequence) - window_size + 1):
                sequence = tuple(self.current_sequence[i:i + window_size])
                
                # Find all occurrences of this sequence
                occurrences = []
                for j in range(len(self.current_sequence) - window_size + 1):
                    if j != i and self.current_sequence[j:j + window_size] == list(sequence):
                        start_line = self.line_mappings[j][0]
                        end_line = self.line_mappings[j + window_size - 1][1]
                        occurrences.append((start_line, end_line))
                
                if occurrences:
                    # Add the original occurrence
                    start_line = self.line_mappings[i][0]
                    end_line = self.line_mappings[i + window_size - 1][1]
                    occurrences.insert(0, (start_line, end_line))
                    
                    all_duplicates.append(DuplicateInfo(
                        structure=list(sequence),
                        occurrences=occurrences,
                        node_count=window_size
                    ))
        
        # Filter out overlapping duplicates
        filtered_duplicates = self._filter_overlapping_duplicates(all_duplicates)
        
        # Calculate duplication percentage based on actual lines of code
        total_significant_lines = self._count_significant_lines(code)
        
        duplicated_lines = set()
        for dup in filtered_duplicates:
            for start, end in dup.occurrences[1:]:  # Skip first occurrence
                for line_num in range(start, end + 1):
                    line = code.splitlines()[line_num - 1].strip()
                    if line and not line.startswith('#') and not (line.startswith('"""') and line.endswith('"""')):
                        duplicated_lines.add(line_num)
        
        duplication_percentage = (len(duplicated_lines) / total_significant_lines * 100) if total_significant_lines > 0 else 0
        
        return filtered_duplicates, duplication_percentage

def format_duplicate_report(duplicates: List[DuplicateInfo], duplication_percentage: float) -> str:
    if not duplicates:
        return "No se encontraron duplicados estructurales significativos.\nPorcentaje de duplicación: 0%"
    
    report = []
    report.append("=== REPORTE DE DUPLICACIÓN ESTRUCTURAL ===\n")
    report.append(f"Porcentaje de líneas duplicadas: {duplication_percentage:.2f}%\n")
    
    for i, dup in enumerate(duplicates, 1):
        report.append(f"\nDuplicado #{i}:")
        report.append(f"Número de nodos: {dup.node_count}")
        report.append("Patrón estructural:")
        report.append("```")
        report.append(" → ".join(dup.structure))
        report.append("```")
        
        report.append("\nOcurrencias:")
        for start, end in dup.occurrences:
            report.append(f"- Líneas {start}-{end}")
        
        report.append("-" * 50)
    
    return "\n".join(report)

def analyze_file(file_path: str, min_length: int = 3) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            code = file.read()
        
        detector = StructuralDuplicateDetector()
        duplicates, duplication_percentage = detector.analyze_code(code, min_length)
        return format_duplicate_report(duplicates, duplication_percentage)
    
    except FileNotFoundError:
        return f"Error: No se encontró el archivo '{file_path}'"
    except Exception as e:
        return f"Error al procesar el archivo: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description='Detector de duplicación estructural en código Python')
    parser.add_argument('file', help='Archivo a analizar')
    parser.add_argument('--min-length', type=int, default=3,
                      help='Longitud mínima de secuencia para considerar duplicado (default: 3)')
    
    args = parser.parse_args()
    print(analyze_file(args.file, args.min_length))

if __name__ == "__main__":
    main()