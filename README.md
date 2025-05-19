# ETL COVID Cundiboy

Este proyecto carga datos de COVID desde archivos CSV a una base de datos MySQL en la nube (GCP).

## 🚀 Dashboard en vivo

[👉 Accede al dashboard COVID Cundiboy](https://covid-dashboard-cundiboy.streamlit.app)

Visualiza indicadores clave (contagios, recuperaciones, fallecimientos, tasas e indicadores por edad), con filtros interactivos por fecha, municipio, departamento, género y tipo de contagio.

## Requisitos

- Python 3.8+
- Acceso a la base de datos MySQL (IP pública, usuario y contraseña)
- Dependencias listadas en `requirements.txt`

## Instrucciones

1. Clona el repositorio
2. Coloca los archivos `.csv` en la carpeta `data/`
3. Configura la conexión a la base de datos en `db_config.py`
4. Instala las dependencias: `pip install -r requirements.txt`
5. Ejecuta una de las siguientes opciones:
- Para cargar datos sin borrar los existentes: `python etl.py`
- Para borrar todos los datos antes de cargar: `python etl.py --borrar`

## 🧾 Formato esperado de los archivos CSV

- **department.csv**  
  `id_department;name`

- **municipality.csv**  
  `id_municipality;name_municipality;id_department`

- **gender.csv**  
  `id_gender;name`

- **type_contagion.csv**  
  `id_type;name`

- **status.csv**  
  `id_status;name`

- **cases.csv**  
  `id_case;id_municipality;age;id_gender;id_type;id_status;date_symptom;date_death;date_diagnosis;date_recovery`

> El archivo `cases.csv` se ajusta automáticamente para que `id_type` se renombre a `id_type_contagion` y `date_symptom` a `date_symptoms`.
