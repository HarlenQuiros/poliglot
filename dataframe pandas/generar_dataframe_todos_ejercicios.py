import os
import pandas as pd

file_name = "a.xlsx"
file_path = os.path.join(os.getcwd(), file_name)


print(f"Usando archivo: {file_path}")


xls = pd.ExcelFile(file_path)
dfs = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in ['Ejercicio1', 'Ejercicio2', 'Ejercicio3', 'Ejercicio4']}

def clean_df(df):
    if df.columns.str.contains("Unnamed").sum() > 3:
        df.columns = df.iloc[0]
        df = df[1:]
    return df

dfs['Ejercicio2'] = clean_df(dfs['Ejercicio2'])
dfs['Ejercicio3'] = clean_df(dfs['Ejercicio3'])

combined_all = pd.concat([dfs['Ejercicio1'], dfs['Ejercicio2'], dfs['Ejercicio3'], dfs['Ejercicio4']], ignore_index=True)

comment_cols = [col for col in combined_all.columns if 'Coment' in col]
combined_all['Comentario Final'] = combined_all[comment_cols].astype(str).apply(lambda row: ' '.join(row.values), axis=1).str.strip()
combined_all_clean = combined_all.drop(comment_cols, axis=1)

print(combined_all_clean.head())

# Save the cleaned DataFrame to a CSV file
# combined_all_clean.to_excel("metricas_completas.xlsx", index=False)
combined_all_clean.to_csv("metricas_completas.csv", index=False)