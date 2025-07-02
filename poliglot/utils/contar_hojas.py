import pandas as pd

def contar_hojas_por_carnets(ruta_excel, carnets_buscar):
    # Cargar el archivo Excel
    df = pd.read_excel(ruta_excel)
    df["Carné de estudiante"] = df["Carné de estudiante"].astype(str).str.lstrip("'")
    df["Start time"] = pd.to_datetime(df["Start time"], format="%d/%m/%Y %H:%M:%S", errors="coerce")
    df["Solo fecha"] = df["Start time"].dt.date


    # Filtrar solo las filas con carnets que están en la lista
    # df_filtrado = df[df["Carné de estudiante"].isin(carnets_buscar)]

    # Contar cuántos son de cada hoja
    conteo_hojas = df["¿Cuál hoja de ejercicios desarrolló?"].value_counts()

    # Obtener los valores específicos (o 0 si no están)
    hoja_a = conteo_hojas.get("A", 0)
    hoja_b = conteo_hojas.get("B", 0)

    print(f"Cantidad de estudiantes con Hoja A: {hoja_a}")
    print(f"Cantidad de estudiantes con Hoja B: {hoja_b}")

    # Conteo por fecha y hoja
    conteo_por_fecha = df.groupby(["Solo fecha", "¿Cuál hoja de ejercicios desarrolló?"]).size().unstack(fill_value=0)

    print("\n=== Conteo por fecha ===")
    print(conteo_por_fecha)

# === EJEMPLO DE USO ===

# Ruta al archivo Excel (puede ser .xlsx o .xls)
ruta_archivo = "./poliglot/actividad.xlsx"

# Lista de carnets a buscar (puedes modificarla con los carnets que desees)
lista_carnets = [
    "2024093410", "2024090884", "2022000033", "2020184824",
    "2024099007", "2024192981", "2024256560", "2024800158",
    "2024109692", "2024112230", "2024114502", "2024136072",
    "2024138712", "2024140841", "2024145153", "2024178193",
    "2024178653", "2024192981", "2024202804", "2024252331",
    "2024253395", "2024253434", "2024256560", "2024800088",
    "2024800128", "2024800158", "2024800621", "2024800990",
    "2022146515", "2023152721", "2024063271", "2024066829",
    "2024071983", "2024096731"
]




contar_hojas_por_carnets(ruta_archivo, lista_carnets)
