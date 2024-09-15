import tempfile
import re
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from analyze.excel import analyze_group, analyze_student

gauth = GoogleAuth()
gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.
drive = GoogleDrive(gauth)

# Get the contents of a folder and subfolders
def process_files_in_folder(file_list):
    for file in file_list:
        if file['mimeType'] == 'application/vnd.google-apps.folder':
            if not re.search(r'(consentimientos|proyecto)', file['title'], re.IGNORECASE):  # Skip folders with consent forms or projects
                print(f"Carpeta: {file['title']} (ID: {file['id']})")
                # Recursive call to process the subfolder
                query = f"'{file['id']}' in parents and trashed=false"
                sub_file_list = drive.ListFile({'q': query}).GetList()
                process_files_in_folder(sub_file_list)
        else:
            print(f"  Archivo: {file['title']} (ID: {file['id']})")


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
    
    print(f"Contenido de la carpeta '{dir[-1]}':")
    process_files_in_folder(file_list)