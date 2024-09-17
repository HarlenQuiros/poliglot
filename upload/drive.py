import tempfile
import re
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from analyze.excel import analyze_group, analyze_student

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
    

def search_for_sentence(file_list, year, semester, course_code, group_number):
    global file_counter
    for file in file_list:
        if file['mimeType'] == 'application/pdf' and file['title'] == 'enunciado.pdf':
            with tempfile.TemporaryDirectory() as tmp_dir:
                file_path = f"{tmp_dir}/enunciado.pdf"
                file.GetContentFile(file_path)
            return file_path
    return None
            

# Get the contents of a folder and subfolders
def process_files_in_folder(file_list, year, semester, course_code, group_number, sentence=None):
    if sentence is None:
        sentence = search_for_sentence(file_list, year, semester, course_code, group_number)

    for file in file_list:
        if file['mimeType'] == 'application/vnd.google-apps.folder':
            if not re.search(r'(proyecto)', file['title'], re.IGNORECASE):  # Skip folders with consent forms or projects
                # Recursive call to process the subfolder
                query = f"'{file['id']}' in parents and trashed=false"
                sub_file_list = drive.ListFile({'q': query}).GetList()
                process_files_in_folder(sub_file_list, year, semester, course_code, group_number, sentence)


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
    
    get_students(file_list) # Better skip if the students are already in BD, otherwise your genderize's requests will be wasted
"""
    # process the subfolders in the final directory 
    for file in file_list:
        if file['mimeType'] == 'application/vnd.google-apps.folder' and not re.search(r'(consentimientos)', file['title'], re.IGNORECASE):
            course_code = file['title'][:7]
            
            try:
                group_number = int(file['title'][-2:])
            except:
                print(f"Error: Wrong group number format in subfolder.")
                return
            
            query = f"'{file['id']}' in parents and trashed=false"
            sub_file_list = drive.ListFile({'q': query}).GetList()
            process_files_in_folder(sub_file_list, year, semester, course_code, group_number)"""
