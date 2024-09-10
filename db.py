import pyodbc

conn_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=Poliglot;UID=sa;PWD=.,%I4(X09Lko;'

def set_groups(group):
    try:
        conn = pyodbc.connect(conn_string)
        cursor = conn.cursor()
        cursor.execute("EXEC SP_Insert_Group ?, ?, ?, ?, ?, ?, ?", 
                    group['Año'], 
                    group['Semestre'], 
                    group['Código'], 
                    group['Curso'], 
                    group['Grupo'], 
                    group['Docente'], 
                    group['Sede'])
        conn.commit()
    except Exception as e:
        print(f"Failure inserting data: {e}")
    finally:
        cursor.close()
        conn.close()


def set_student(group):
    try:
        conn = pyodbc.connect(conn_string)
        cursor = conn.cursor()
        cursor.execute("EXEC SP_Insert_Student ?, ?, ?, ?", 
                    group['Carné'], 
                    group['Nombre'],
                    1, 
                    group['Género'],)
        conn.commit()
    except Exception as e:
        print(f"Failure inserting data: {e}")
    finally:
        cursor.close()
        conn.close()
