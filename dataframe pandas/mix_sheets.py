import os
import pandas as pd

df1 = pd.read_excel("Lista_ejercicio_nombre_carnet.xlsx", sheet_name="Sheet1")

df2 = pd.read_excel("Evaluacion_rondas_consensuado.xlsx", sheet_name="Evaluacion ABS", header=None)
df2.columns = ["Ex", "Evaluador #1", "Comentario #1", "Evaluador #2", "Comentario #2", "Evaluador #3", "Comentario #3", "Trash"]

df3 = pd.read_excel("Clasificación_y_métricas de soluciones.xlsx", sheet_name="Compress 2")

df1["key"] = df1["Archivo"].str.extract(r'(\d+)').astype(int)
df2["key"] = df2["Ex"].str.extract(r'(\d+)').fillna(0).astype(int)

merged_df = pd.merge(df1, df2, on="key", how="inner")
merged_df = merged_df.drop(columns=["Ex","Comentario #1", "Evaluador #2", "Comentario #2", "Evaluador #3", "Comentario #3", "Trash", "Nombre", "Archivo", "Ejercicio", "Grupo", "Corre", "Resuelve", "Métricas"])

df3["Key"] = df3.iloc[:, 0]

merged_df = df3.merge(merged_df[["Carnet", "Evaluador #1"]], left_on="Key", right_on="Carnet", how="left")
merged_df.iloc[:, 1] = merged_df["Evaluador #1"]

merged_df = merged_df.drop(columns=["Carnet", "Evaluador #1", "Key"])

merged_df.to_excel("temporal.xlsx", index=False)