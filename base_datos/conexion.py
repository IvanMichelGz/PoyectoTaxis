import pyodbc

def obtener_conexion():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=IVANMICHEL07XD;"
        "DATABASE=TAXISUNI;"
        "UID=sa;"
        "PWD=Ivan123;"
    )