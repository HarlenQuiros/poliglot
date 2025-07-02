import os
import ast
import builtins
import stanza
import re

# Stemming
from nltk.stem import PorterStemmer

# Translate 
from deep_translator import GoogleTranslator

# Lazy-load stanza pipeline only when needed
_nlp = None
def get_nlp():
    global _nlp
    if _nlp is None:
        _nlp = stanza.Pipeline('en', download_method='none')
    return _nlp

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
    nlp = get_nlp()
    doc = nlp(text)
    unique_words = set()
    for sentence in doc.sentences:
        for word in sentence.words:
            if word.pos == 'NOUN' or word.pos == 'ADJ' or word.pos == 'VERB':
                unique_words.add(word.lemma.lower())
    return lemmatize_words(translate_words(list(unique_words)))

def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    
    return intersection / union

def get_comments(code):
    comments = []
    # Tokenize the code
    # Regex para comentarios de una línea
    comentarios_unilinea = re.findall(r'#.*$', code, re.MULTILINE)

    # Regex para comentarios multilínea
    comentarios_multilinea = re.findall(r'("""(.*?)"""|\'\'\'(.*?)\'\'\')', code, re.DOTALL)

    for comentario in comentarios_unilinea:
        comentario = comentario[1:]
        comentario = comentario.strip()
        comments.append(comentario)
    
    for comentario in comentarios_multilinea:
        comments.append(comentario[1].strip())

    comment_words = set()
    for comment in comments:
        words = re.split(r'[ \n]+', comment)
        print("Words: ", words)
        words = lemmatize_words(translate_words(words))
        comment_words.update(words)
    return comment_words

def analyze_sustej(file_path, enunciado):
        with open(file_path, 'r', encoding='utf-8') as file:
            code = file.read()
        variables = analyze_code_case_frequency(code)
        comments = get_comments(code)
        res_variables = jaccard_similarity(enunciado, variables)
        res_comments = jaccard_similarity(enunciado, comments)
        output = []
        output.append(f"Jaccard variables: {res_variables:.2f}")
        output.append(f"Jaccard comments: {res_comments:.2f}")
        return '\n'.join(output)

def analyze_directory_sustej(directory_path, enunciado):
    results = {}
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    results[file_path] = analyze_sustej(file_path, enunciado)
                except Exception as e:
                    results[file_path] = f"Error: {e}"
    return results

def run_coherence_metrics(path, statement_file):
    import os
    if not os.path.isfile(statement_file):
        return f"Statement file not found: {statement_file}"
    with open(statement_file, 'r', encoding='utf-8') as f:
        statement_text = f.read()
    # Only translate and process statement once
    statement_text_en = translate_text(statement_text, source_language='es', target_language='en')
    enunciado = get_nouns(statement_text_en)
    
    if os.path.isfile(path):
        try:
            return {path: analyze_sustej(path, enunciado)}
        except Exception as e:
            return {path: f"Error: {e}"}
    elif os.path.isdir(path):
        return analyze_directory_sustej(path, enunciado)
    else:
        return {path: f"Invalid path: {path}"}