import pyodbc
from dotenv import load_dotenv
import os

load_dotenv()
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')
conn_string = f'DRIVER={{MySQL ODBC 9.0 Unicode Driver}};SERVER={db_host};PORT={db_port};DATABASE={db_name};UID={db_user};PWD={db_password};'


def execute_query_without_return(query, params):
    try:
        conn = pyodbc.connect(conn_string)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
    except pyodbc.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        try:
            cursor.close() 
            conn.close()
        except: pass


def execute_query_with_return(query, params):
    try:
        conn = pyodbc.connect(conn_string)
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        return results
    except pyodbc.Error as e:
        print(f"Database error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass


def set_groups(group):
    query = "CALL SP_Insert_Group(?, ?, ?, ?, ?, ?, ?)"
    params = (  
        group['Año'], 
        group['Semestre'], 
        group['Código'], 
        group['Curso'], 
        group['Grupo'], 
        group['Docente'], 
        group['Sede']
    )
    execute_query_without_return(query, params)


def set_student(group):
    query = "CALL SP_Insert_Student(?, ?, ?, ?, ?)"
    params = (
        group['Carné'], 
        group['Nombre'],
        1, 
        group['Género'],
        group['Correo electrónico']
    )
    execute_query_without_return(query, params)


def set_exercise(name, statement, year, semester, course_code, group_number):
    query = "CALL SP_Insert_Exercise(?, ?, ?, ?, ?, ?)"
    params = (
        name,
        statement, 
        year, 
        semester, 
        course_code,
        group_number
    )
    value = execute_query_with_return(query, params)[0][0]
    print(f"Statement ID: {value}")
    return value
