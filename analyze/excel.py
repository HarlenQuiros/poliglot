import pandas as pd
from db import set_groups, set_student
from genderize import predict_gender

def analyze_group(file):
    df = pd.read_excel(file, skiprows=6)
    df.columns = df.columns.str.strip()
    course_data = df[['Año', 'Semestre', 'Código', 'Curso', 'Grupo', 'Docente', 'Sede']]
    course_data = course_data.dropna() # Remove empty rows
    
    for index, row in course_data.iterrows():
        set_groups(row)
    
    print("Groups inserted successfully.")


def analyze_student(file):
    df = pd.read_excel(file, skiprows=8)
    df.columns = df.columns.str.strip()
    course_data = df[['Carné', 'Nombre', 'Correo electrónico']]
    course_data = course_data.dropna() # Remove empty rows
    
    for index, row in course_data.iterrows():
        row['Género'] = 'male'
        set_student(row)
    
    print("Student inserted successfully.")
