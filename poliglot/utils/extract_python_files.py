import os
import pandas as pd
import argparse

def save_python_files_from_excel(file_path, output_dir):
    df = pd.read_excel(file_path)
    cols = [
        "Carné de estudiante",
        "¿Cuál hoja de ejercicios desarrolló?",
        "Pegue acá la solución al\xa0Ejercicio #1 (código en Python)",
        "Pegue acá la solución al\xa0Ejercicio #2 (código en Python)",
        "Pegue acá la solución al\xa0Ejercicio #3 (código en Python)",
        "Opcional: Pegue acá la solución al\xa0Ejercicio #4 (código en Python)"
    ]
    df = df[cols]

    etiqueta_mapping = {
        ("A", 1): 1, ("A", 2): 2, ("A", 3): 3, ("A", 4): 4,
        ("B", 1): 1, ("B", 2): 3, ("B", 3): 4, ("B", 4): 2
    }

    for _, row in df.iterrows():
        carnet = str(row["Carné de estudiante"]).strip()
        type = str(row["¿Cuál hoja de ejercicios desarrolló?"]).strip()

        for i in range(1, 5):
            col_name = f"Pegue acá la solución al\xa0Ejercicio #{i} (código en Python)"
            if i == 4:
                col_name = f"Opcional: {col_name}"
            if col_name in row and pd.notna(row[col_name]):
                code = row[col_name]
                # folder_path = os.path.join(output_dir, type, f"Ejercicio{i}")
                etiqueta = etiqueta_mapping.get((type, i), None)
                if etiqueta is None:
                    print(f"Error: No se encontró la etiqueta para {type} y Ejercicio {i}")
                    continue

                folder_path = os.path.join(output_dir, f"{etiqueta}")

                # Make folder if it doesn't exist
                os.makedirs(folder_path, exist_ok=True)
                file_path = os.path.join(folder_path, f"{carnet}.py")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(str(code))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("excel_path", type=str, help="Path to the excel file")
    args = parser.parse_args()
    output_directory = "./codes"
    save_python_files_from_excel(args.excel_path, output_directory)
    print("Archivos generados exitosamente.")
