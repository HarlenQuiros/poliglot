import os
import pandas as pd

df1 = pd.read_csv("Mapeo_estudiantes_anonimizado.csv", encoding="cp1252", sep=";")
df2 = pd.read_excel("Clasificación_y_métricas de soluciones.xlsx", sheet_name="Compress 2", header=1)

merged_df = pd.merge(df1, df2, left_on="# de carnet", right_on="Carnet", how="right")
merged_df = merged_df[(merged_df["Tipo de ejercicio"] == 2)]
merged_df["Nivel_Abstracción_MANUAL profes"] = merged_df["Evaluación Manual"]
merged_df = merged_df.drop(columns=["Evaluación Manual"])

merged_df.to_excel("2.xlsx", index=False, sheet_name="Compress 2")

df2 = pd.read_excel("Clasificación_y_métricas de soluciones.xlsx", sheet_name="Zoologico 1", header=1)
merged_df = pd.merge(df1, df2, left_on="# de carnet", right_on="Carnet", how="right")
merged_df = merged_df[(merged_df["Tipo de ejercicio"] == 1)]
merged_df["Nivel_Abstracción_MANUAL profes"] = merged_df["Evaluación Manual"]
merged_df = merged_df.drop(columns=["Evaluación Manual"])

merged_df.to_excel("1.xlsx", index=False, sheet_name="Zoologico 1")

df2 = pd.read_excel("Clasificación_y_métricas de soluciones.xlsx", sheet_name="Conteo 3", header=1)
merged_df = pd.merge(df1, df2, left_on="# de carnet", right_on="Carnet", how="right")
merged_df = merged_df[(merged_df["Tipo de ejercicio"] == 3)]
merged_df["Nivel_Abstracción_MANUAL profes"] = merged_df["Evaluación Manual"]
merged_df = merged_df.drop(columns=["Evaluación Manual"])
merged_df["Evaluación SOLO"] =merged_df["SOLO"]
merged_df = merged_df.drop(columns=["SOLO"])

merged_df.to_excel("3.xlsx", index=False, sheet_name="Conteo 3")

df2 = pd.read_excel("Clasificación_y_métricas de soluciones.xlsx", sheet_name="Shiritori 4", header=1)
merged_df = pd.merge(df1, df2, left_on="# de carnet", right_on="Carnet", how="right")
merged_df = merged_df[(merged_df["Tipo de ejercicio"] == 4)]
merged_df["Nivel_Abstracción_MANUAL profes"] = merged_df["Evaluación Manual"]
merged_df = merged_df.drop(columns=["Evaluación Manual"])
merged_df["Evaluación SOLO"] =merged_df["SOLO"]
merged_df = merged_df.drop(columns=["SOLO"])

merged_df.to_excel("4.xlsx", index=False, sheet_name="Shiritori 4")