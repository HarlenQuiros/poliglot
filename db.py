import pyodbc

conn_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=Poliglot;UID=sa;PWD=.,%I4(X09Lko;'

def execute_query_without_return(query, params):
    try:
        conn = pyodbc.connect(conn_string)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
    except Exception as e:
        print(f"Failure inserting data: {e}")
    finally:
        cursor.close()
        conn.close()

def set_groups(group):
    query = "EXEC SP_Insert_Group ?, ?, ?, ?, ?, ?, ?",
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
    query = "EXEC SP_Insert_Student ?, ?, ?, ?",
    params = (
        group['Carné'], 
        group['Nombre'],
        1, 
        group['Género'],)
    execute_query_without_return(query, params)
