import os
import ast
import builtins
import stanza
import re
import tokenize
import io

# Stemming
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

# Translate 
from deep_translator import GoogleTranslator

# stanza.download('en')

def translate_words(words):
    translator = GoogleTranslator(source='es', target='en')
    translated_words = set()  # Use a set for unique words
    for word in words:
        translation = translator.translate(word)
        if translation is not None:
            translated_words.add(translation.lower())  # Add translated word in lowercase
    return translated_words

def translate_text(text, source_language='es', target_language='en'):
    """
    Translates a given text from the source language to the target language using deep-translator.

    Parameters:
    text (str): The text to be translated.
    source_language (str): The language of the input text (default is 'auto' for automatic detection).
    target_language (str): The language to translate the text into (default is 'en' for English).

    Returns:
    str: The translated text.
    """
    try:
        translated_text = GoogleTranslator(source=source_language, target=target_language).translate(text)
        return translated_text
    except Exception as e:
        print(f"Error during translation: {e}")
        return None

def lemmatize_words(words):
    ps = PorterStemmer()
    lemmatized_words = [ps.stem(word) for word in words]
    return set(lemmatized_words)

def analyze_code_case_frequency(code):
    # print(code)
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

    variables = lemmatize_words(translate_words(list(identifiers)))
    return variables

def get_nouns(text):
    # Process the text
    doc = nlp(text)
    
    unique_words = set()
    
    # Print only the nouns (POS: NOUN for common nouns, PROPN for proper nouns)
    for sentence in doc.sentences:
        for word in sentence.words:
            if word.pos == 'NOUN' or word.pos == 'ADJ' or word.pos == 'VERB':
                unique_words.add(word.lemma.lower())
    return lemmatize_words(translate_words(list(unique_words)))

def jaccard_similarity(set1, set2):
	# intersection of two sets
	intersection = len(set1.intersection(set2))
	# Unions of two sets
	union = len(set1.union(set2))
	
	return intersection / union

def get_comments(code):
    comments = []
    # Tokenize the code
    # Regex para comentarios de una línea
    comentarios_unilinea = re.findall(r'#.*$', code, re.MULTILINE)

    # Regex para comentarios multilínea
    comentarios_multilinea = re.findall(r'("""(.*?)"""|\'\'\'(.*?)\'\'\')', code, re.DOTALL)

    # Imprimir resultados
    # print("Comentarios de una línea:")
    for comentario in comentarios_unilinea:
        # print(type(comentario), len(comentario))
        comentario = comentario[1:]
        comentario = comentario.strip()
        comments.append(comentario)

    # print("\nComentarios multilínea:")
    for comentario in comentarios_multilinea:
        # print(type(comentario), len(comentario), comentario)
        comments.append(comentario[1].strip())

    # print("Comments: ", comments)
    # tokens = tokenize.tokenize(io.BytesIO(code.encode('utf-8')).readline)
    # for token in tokens:
    #     if token.type == tokenize.COMMENT:
    #         comments.append(token.string)

    comment_words = set()
    for comment in comments:
        words = re.split(r'[ \n]+', comment)
        print("Words: ", words)
        words = lemmatize_words(translate_words(words))
        comment_words.update(words)
    #     words = word_tokenize(comment)
    #     for word in words:
    #         comment_words.add(word.lower())
    return comment_words

def analyze_codes():
    enunciado = get_nouns(texto)
    print("Enunciado: ", enunciado)
    values_variables = []
    values_comments = []
    result_file = open('result.txt', 'w', encoding='utf-8')
    file_path = r'.\codes'
    py_files = [f for f in os.listdir(file_path) if f.endswith('.py')]
    for file in py_files:
        with open(file_path + '\\' + file, 'r', encoding='utf-8') as file:
            code = file.read()
            variables = analyze_code_case_frequency(code)
            comments = get_comments(code)
            res_variables = jaccard_similarity(enunciado, variables)
            print("Comments: ", comments)
            res_comments = jaccard_similarity(enunciado, comments)
            values_variables.append("Carnet: " + file.name + " - " + str(res_variables) + '\n')
            values_comments.append("Carnet: " + file.name + " - " + str(res_comments) + '\n')

    result_file.write("Variables:\n")
    result_file.write(', '.join(values_variables) + '\n\n')
    result_file.write("Comentarios:\n")
    result_file.write(', '.join(values_comments) + '\n')
    

# Initialize the Spanish NLP pipeline
#stanza.download('en') 
nlp = stanza.Pipeline('en', download_method='none')

texto = """Desarrolle la función listas_ordenadas. Recibe una lista de n números y retorna una
lista con sublistas de secuencias ascendentes y descendentes presentes en la
lista recibida. Una secuencia está formada por una serie de números seguidos que presentan
un determinado orden, ya sea de menor a mayor (ascendente) o de mayor a menor
(descendente), y termina cuando el número siguiente en la lista de entrada cambia el orden
que se está construyendo Ejemplos del funcionamiento:"""

texto = translate_text(texto, source_language='es', target_language='en')

analyze_codes()
#print("Texto: "+ translate_text(texto, source_language='es', target_language='en'))