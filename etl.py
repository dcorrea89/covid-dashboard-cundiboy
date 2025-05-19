import pandas as pd
import sys
from db_config import get_engine
from sqlalchemy import text

# Diccionario para la carga ordenada
csv_files = {
    "department": "data/department.csv",
    "municipality": "data/municipality.csv",
    "gender": "data/gender.csv",
    "type_contagion": "data/type_contagion.csv",
    "status": "data/status.csv",
    "cases": "data/cases.csv"
}

# Orden para eliminar datos (tablas hijas primero)
tablas_en_orden_borrado = [
    "cases",
    "municipality",
    "department",
    "gender",
    "status",
    "type_contagion"
]

def borrar_datos():
    engine = get_engine()
    with engine.begin() as conn:
        for tabla in tablas_en_orden_borrado:
            print(f"Borrando datos de {tabla}...")
            conn.execute(text(f"DELETE FROM {tabla}"))
        print("✔ Todos los datos fueron eliminados correctamente.\n")

def cargar_tabla(nombre_tabla, path_archivo):
    print(f"Cargando {nombre_tabla} desde {path_archivo}...")
    df = pd.read_csv(path_archivo, sep=';')

    # Ajuste de columnas
    if nombre_tabla == "municipality":
        df.rename(columns={"name_municipality": "name"}, inplace=True)
    elif nombre_tabla == "type_contagion":
        df.rename(columns={"id_type": "id_type_contagion"}, inplace=True)
    elif nombre_tabla == "cases":
        df.rename(columns={
            "id_type": "id_type_contagion",
            "date_symptom": "date_symptoms"
        }, inplace=True)

    engine = get_engine()
    df.to_sql(nombre_tabla, con=engine, if_exists='append', index=False)
    print(f"✔ {nombre_tabla} cargada correctamente.\n")

def main():
    if "--borrar" in sys.argv:
        borrar_datos()
    for tabla, archivo in csv_files.items():
        cargar_tabla(tabla, archivo)

if __name__ == "__main__":
    main()
