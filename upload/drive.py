import tempfile
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from analyze.excel import analyze_group, analyze_student

gauth = GoogleAuth()
gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.
drive = GoogleDrive(gauth)

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

    with tempfile.TemporaryDirectory() as tmp_dir:
        for file in file_list: 
            # Process only Excel files
            if file['mimeType'] == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                file_path = f"{tmp_dir}/{file['title']}"
                file.GetContentFile(file_path)
                analyze_student(file_path)
