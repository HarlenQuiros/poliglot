import pdfplumber
import re
from db import set_exercise

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text


def split_exercises(text):
    return re.split(r'\n(?=\d+\.\s)', text)  # Split by new line followed by a number and a dot


def analyze_statement(pdf_path, case, name, year, semester, course_code, group_number):
    """
    You mustn't delete the code below, it will be useful in the future.
    At the moment, we won't split each statemenet into exercises because of the complexity of the task.
    Most proffesors don't follow a standard format for the exercises.

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
    """
    text = extract_text_from_pdf(pdf_path)

    if case == 1:
        return text
    else:  # case == 2
        return set_exercise(name, text, year, semester, course_code, group_number)
