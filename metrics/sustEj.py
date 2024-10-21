import os
import ast
import builtins
import stanza
import re

def analyze_code_case_frequency(code):
    print(code)
    tree = ast.parse(code)
    identifiers = set()
    builtin_names = dir(builtins)
    pattern = r'(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|[_-]'

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.ClassDef):
            if node.name not in builtin_names: 
                for word in re.split(pattern, node.name):
                    identifiers.add(word.lower())
        elif isinstance(node, ast.Name):
            if node.id not in builtin_names:
                for word in re.split(pattern, node.id):
                    identifiers.add(word.lower())
    print(identifiers)
    return identifiers

def get_nouns(text):
    # Initialize the Spanish NLP pipeline
    nlp = stanza.Pipeline('es')
    
    # Process the text
    doc = nlp(text)
    
    unique_words = set()
    
    # Print only the nouns (POS: NOUN for common nouns, PROPN for proper nouns)
    for sentence in doc.sentences:
        for word in sentence.words:
            if word.pos == 'NOUN' or word.pos == 'ADJ':
                unique_words.add(word.text.lower())
    print(unique_words)
    return unique_words

def jaccard_similarity(set1, set2):
	# intersection of two sets
	intersection = len(set1.intersection(set2))
	# Unions of two sets
	union = len(set1.union(set2))
	
	return intersection / union

def analyze_codes():
    set1 = get_nouns(texto)
    values = []
    result_file = open('result.txt', 'w', encoding='utf-8')
    file_path = r'C:\Users\hdani\OneDrive\Escritorio\Harlen\Asistencia pensamiento computacional\codes'
    py_files = [f for f in os.listdir(file_path) if f.endswith('.py')]
    for file in py_files:
        with open(file_path + '\\' + file, 'r', encoding='utf-8') as file:
            code = file.read()
            res = jaccard_similarity(set1, analyze_code_case_frequency(code))
            values.append("Carnet: " + file.name + " - " + str(res) + '\n')
    result_file.write("Resultados:\n")
    result_file.write(', '.join(values) + '\n\n')
    

texto = """Escriba una función llamada repetidos (L) que reciba como argumento una lista L no vacía de
elementos y retorne la lista de elementos que están repetidos en la lista. Si el elemento se encuentra
repetido más de una vez en L, sólo debe aparecer una vez en la lista de resultado. La función debe
lanzar una excepción en caso de que no se cumpla alguna de las restricciones. No se permite el uso
del tipo set, ni de ningún tipo de iteración (for o while). Utilice recursión de cola. No es necesario
crear un programa principal para utilizar esta función."""

analyze_codes()