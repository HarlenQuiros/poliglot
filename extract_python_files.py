import os
import pandas as pd
import argparse

def save_python_files_from_excel(file_path, output_dir):
    df = pd.read_excel(file_path)
    cols = [
        "Carné de estudiante",
        "¿Cuál hoja de ejercicios desarrolló?",
        "Pegué acá la solución al\xa0Ejercicio #1 (código en Python)",
        "Pegué acá la solución al\xa0Ejercicio #2 (código en Python)",
        "Pegué acá la solución al\xa0Ejercicio #3 (código en Python)",
        "Opcional: Pegué acá la solución al\xa0Ejercicio #4 (código en Python)"
    ]
    df = df[cols]
    
    for _, row in df.iterrows():
        carnet = str(row["Carné de estudiante"]).strip()
        folder_path = os.path.join(output_dir, str(row["¿Cuál hoja de ejercicios desarrolló?"].strip()))
        
        # Make folder if it doesn't exist
        os.makedirs(folder_path, exist_ok=True)
        
        for i in range(1, 5):
            col_name = f"Pegué acá la solución al\xa0Ejercicio #{i} (código en Python)"
            if i == 4:
                col_name = f"Opcional: {col_name}"
            if col_name in row and pd.notna(row[col_name]):
                code = row[col_name]
                file_path = os.path.join(folder_path, f"{carnet}_Ejercicio{i}.py")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(str(code))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("excel_path", type=str, help="Path to the excel file")
    args = parser.parse_args()
    output_directory = "./codes"
    save_python_files_from_excel(args.excel_path, output_directory)
    print("Archivos generados exitosamente.")
