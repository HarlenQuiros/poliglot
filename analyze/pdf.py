import pdfplumber
import re

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text


def split_exercises(text):
    return re.split(r'\n(?=\d+\.\s)', text)  # Split by new line followed by a number and a dot


def analyze_statement(pdf_path, case):
    index = dict()

    if case == 1:
        exercises = split_exercises(extract_text_from_pdf(pdf_path))
        for exercise in exercises[1:]: # Skip header
            exercise = exercise.strip() # Avoid exercises empty
            if exercise:
                # Get the exercise name
                start = exercise.find('.') + 2
                end = exercise.find('\n')
                name = exercise[start:end]
                name = re.sub(r'\s*\(.*\)\s*$', '', name) # Delete amount of points
                index[name] = exercise
    else: # case == 2
        text = extract_text_from_pdf(pdf_path)
