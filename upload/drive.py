import tempfile
import re
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from analyze.excel import analyze_group, analyze_student, analyze_aspects, analyze_grade
from analyze.pdf import analyze_statement
from db import set_exercise, set_solution

gauth = GoogleAuth()
gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.
drive = GoogleDrive(gauth)

def extract_info_from_path(dir):
    try:
        year = dir[1][:4]
        semester = dir[1][5]
        return int(year), int(semester)
    except:
        print("Error: Wrong path format, it must be \"DATOS/year-semester...\".")
        return None, None


# Case 1: Several files per student and per sentence
# Case 2: Just one file per student and per sentence
# Otherwise: None
def determine_case(file_list):
    for file in file_list:
        if file['mimeType'] == 'application/vnd.google-apps.folder' and file['title'].startswith('20'):
            return 1
        if file['mimeType'] == 'text/x-python':
            return 2
    return None


def search_for_grade(file_list, case):
    for file in file_list:
        if file['mimeType'] == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' and file['title'] == 'desglose.xlsx':
            with tempfile.TemporaryDirectory() as tmp_dir:
                file_path = f"{tmp_dir}/desglose.xlsx"
                file.GetContentFile(file_path)
                return analyze_grade(file_path, case)


def search_for_aspects(file_list, name, exercise):
    for file in file_list:
        if file['mimeType'] == 'text/csv' and file['title'] == name + '.csv':
            with tempfile.TemporaryDirectory() as tmp_dir:
                file_path = f"{tmp_dir}/aspectos.csv"
                file.GetContentFile(file_path)
                analyze_aspects(file_path, exercise)
    

def search_for_statement(file_list, year, semester, course_code, group_number, case):
    for file in file_list:
        if file['mimeType'] == 'application/pdf' and file['title'] == 'enunciado.pdf':
            # First we get the parent folder title of the file to use it as the name of the exercise
            parent_id = file['parents'][0]['id']
            parent_folder = drive.CreateFile({'id': parent_id})
            parent_folder.FetchMetadata()
            root_dir_name = parent_folder['title']
            with tempfile.TemporaryDirectory() as tmp_dir:
                file_path = f"{tmp_dir}/enunciado.pdf"
                file.GetContentFile(file_path)
                return analyze_statement(file_path, case, root_dir_name, year, semester, course_code, group_number)
    return None


def several_files_per_student(file_list, statement, exercises, year, semester, course_code, group_number, student_id):
    grades = search_for_grade(file_list, 1)
    for file in file_list:
        if file['mimeType'] == 'text/x-python':
            title = file['title'][:-3] # Delete .py extension
            # Upload statement if not on db
            if title not in exercises:
                exercises[title] = set_exercise(title, statement, year, semester, course_code, group_number)
            with tempfile.TemporaryDirectory() as tmp_dir:
                file_path = f"{tmp_dir}/{file['title']}"
                file.GetContentFile(file_path)
                set_solution(int(student_id), int(exercises[title]), file_path, int(grades[title]))
            

# Get the contents of a folder and subfolders
def process_files_in_folder(file_list, year, semester, course_code, group_number):
    """This should be with an if statement is null, 
    but that case never happens due to the drive structure.
    We don't do a recursive call when statement is not null"""
    case = determine_case(file_list)
    if case is not None:
        statement = search_for_statement(file_list, year, semester, course_code, group_number, case)
        if statement is not None and case == 1:
            exercises = dict()
        elif statement is not None:  # Extract aspects
            search_for_aspects(file_list, 'keywords', statement)
            grades = search_for_grade(file_list, case)

    for file in file_list:
        if file['mimeType'] == 'application/vnd.google-apps.folder':
            if not re.search(r'(proyecto)', file['title'], re.IGNORECASE):  # Skip folders with projects
                query = f"'{file['id']}' in parents and trashed=false"
                sub_file_list = drive.ListFile({'q': query}).GetList()
                # First case we have multiple files per student and per sentence
                if case == 1 and statement is not None:
                    several_files_per_student(sub_file_list, statement, exercises, year, semester, course_code, group_number, file['title'])
                else:
                    # Recursive call to process the subfolder
                    process_files_in_folder(sub_file_list, year, semester, course_code, group_number)
        # Second case we have just one file per student and per sentence
        elif case == 2 and statement is not None and file['mimeType'] == 'text/x-python':
            title = file['title'][:-3] # Delete .py extension
            title = int(title)
            with tempfile.TemporaryDirectory() as tmp_dir:
                file_path = f"{tmp_dir}/{file['title']}"
                file.GetContentFile(file_path)
                set_solution(title, int(statement), file_path, int(grades[title]))
                
    
    if case == 1 and statement is not None:
        for exercise in exercises:  # Extract aspects
            search_for_aspects(file_list, exercise, exercises[exercise])


def get_groups(path):
    dir = path.split('/') 
    file = None
    parent_id = 'root'

    for name in dir:
        query = f"'{parent_id}' in parents and title = '{name}' and trashed=false"
        file_list = drive.ListFile({'q': query}).GetList()
        
        if len(file_list) == 0:
            print(f"Couldn't find '{name}' in path.")
            return
        
        file = file_list[0]
        parent_id = file['id']  # Next iteration

    if file:
        with tempfile.TemporaryDirectory() as tmp_dir:
            file.GetContentFile(f'{tmp_dir}/profesores.xlsx')
            analyze_group(f'{tmp_dir}/profesores.xlsx')


def get_students(file_list):
    with tempfile.TemporaryDirectory() as tmp_dir:
        for file in file_list: 
            # Process only Excel files
            if file['mimeType'] == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                file_path = f"{tmp_dir}/{file['title']}"
                file.GetContentFile(file_path)
                analyze_student(file_path)


def get_exercises(path):
    dir = path.split('/')
    parent_id = 'root'
    year, semester = extract_info_from_path(dir)
    if year is None:
        return
    
    for name in dir:
        query = f"'{parent_id}' in parents and title = '{name}' and trashed=false"
        file_list = drive.ListFile({'q': query}).GetList()
        
        if len(file_list) == 0:
            print(f"Couldn't find '{name}' in path.")
            return
        
        file = file_list[0]
        parent_id = file['id']  # Next iteration

    # Final directory
    query = f"'{parent_id}' in parents and trashed=false"
    file_list = drive.ListFile({'q': query}).GetList()
    
    # get_students(file_list) # Better skip if the students are already in BD, otherwise your genderize's requests will be wasted

    # process the subfolders in the final directory 
    for file in file_list:
        if file['mimeType'] == 'application/vnd.google-apps.folder' and not re.search(r'(consentimientos)', file['title'], re.IGNORECASE):
            course_code = file['title'][:6]
            
            try:
                group_number = int(file['title'][-2:])
            except:
                print(f"Error: Wrong group number format in subfolder.")
                return
            
            query = f"'{file['id']}' in parents and trashed=false"
            sub_file_list = drive.ListFile({'q': query}).GetList()
            process_files_in_folder(sub_file_list, year, semester, course_code, group_number)
