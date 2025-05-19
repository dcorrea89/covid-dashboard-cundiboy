import pandas as pd
import streamlit as st
import plotly.express as px

# ✅ Solo una vez y al inicio del script
st.set_page_config(page_title="COVID Cundiboy - KPIs", layout="wide")

# Cargar los datos
cases = pd.read_csv("data/cases.csv", sep=';')
status = pd.read_csv("data/status.csv", sep=';')
gender = pd.read_csv("data/gender.csv", sep=';')
type_contagion = pd.read_csv("data/type_contagion.csv", sep=';')
municipality = pd.read_csv("data/municipality.csv", sep=';')
department = pd.read_csv("data/department.csv", sep=';')

# Renombrar columnas para evitar conflictos
gender = gender.rename(columns={"name": "gender_name"})
type_contagion = type_contagion.rename(columns={"name": "contagion_type_name"})
municipality = municipality.rename(columns={"name_municipality": "municipality_name"})
department = department.rename(columns={"name": "department_name"})

# Renombrar en casos
cases.rename(columns={"id_type": "id_type_contagion", "date_symptom": "date_symptoms"}, inplace=True)

# Convertir fechas
for col in ['date_death', 'date_diagnosis', 'date_recovery', 'date_symptoms']:
    cases[col] = pd.to_datetime(cases[col], errors='coerce')

# Uniones
cases = cases.merge(municipality, on='id_municipality', how='left')
cases = cases.merge(department, on='id_department', how='left')
cases = cases.merge(gender, on='id_gender', how='left')
cases = cases.merge(type_contagion, left_on='id_type_contagion', right_on='id_type', how='left')

# Sidebar - Filtros
st.sidebar.header("🔎 Filtros")

# Filtro por fechas
min_date = cases['date_symptoms'].min()
max_date = cases['date_symptoms'].max()
start_date, end_date = st.sidebar.date_input("Rango de fechas de síntomas", [min_date, max_date])

# Filtros selectivos
selected_departments = st.sidebar.multiselect("Departamento", cases['department_name'].dropna().unique())
selected_municipalities = st.sidebar.multiselect("Municipio", cases['municipality_name'].dropna().unique())
selected_genders = st.sidebar.multiselect("Género", cases['gender_name'].dropna().unique())
selected_contagion_types = st.sidebar.multiselect("Tipo de contagio", cases['contagion_type_name'].dropna().unique())

# Aplicar filtros
df = cases.copy()
df = df[(df['date_symptoms'] >= pd.to_datetime(start_date)) & (df['date_symptoms'] <= pd.to_datetime(end_date))]

if selected_departments:
    df = df[df['department_name'].isin(selected_departments)]
if selected_municipalities:
    df = df[df['municipality_name'].isin(selected_municipalities)]
if selected_genders:
    df = df[df['gender_name'].isin(selected_genders)]
if selected_contagion_types:
    df = df[df['contagion_type_name'].isin(selected_contagion_types)]

# KPIs
total_cases = len(df)
total_recovered = df['date_recovery'].notna().sum()
total_deaths = df['date_death'].notna().sum()
fatality_rate = round((total_deaths / total_cases) * 100, 2) if total_cases else 0
recovery_rate = round((total_recovered / total_cases) * 100, 2) if total_cases else 0

df['recovery_days'] = (df['date_recovery'] - df['date_symptoms']).dt.days
avg_recovery_days = round(df['recovery_days'].mean(), 2)

# Agrupar por rango de edad (por década)
df['age_group'] = (df['age'] // 10 * 10).astype(int).astype(str) + 's'
deaths_by_age_group = df[df['date_death'].notna()].groupby('age_group').size()
percent_deaths = (deaths_by_age_group / total_deaths * 100).round(2).reset_index()
percent_deaths.columns = ['Rango de Edad', 'Porcentaje']

# Vista principal
st.title("📊 Dashboard COVID Cundiboy")

# KPIs
st.header("Indicadores Clave de Desempeño (KPIs)")
k1, k2, k3, k4, k5 = st.columns(5)

k1.metric("Total de contagios", f"{total_cases:,}")
k2.metric("Total recuperados", f"{total_recovered:,}")
k3.metric("Total fallecidos", f"{total_deaths:,}")
k4.metric("Tasa de recuperación (%)", f"{recovery_rate}%")
k5.metric("Tasa de letalidad (%)", f"{fatality_rate}%")

st.divider()

# Tiempo promedio de recuperación
st.subheader("⏱ Tiempo promedio de recuperación")
st.write(f"El tiempo promedio de recuperación es de **{avg_recovery_days} días**.")

st.divider()

# Gráfico de fallecidos por edad
st.subheader("⚰️ Porcentaje de fallecidos por rango de edad")
fig = px.bar(percent_deaths, x='Rango de Edad', y='Porcentaje', color='Rango de Edad',
             text='Porcentaje', title="Distribución porcentual de fallecidos por edad")
st.plotly_chart(fig, use_container_width=True)

st.caption("Fuente: Dataset COVID Cundiboy - Datos simulados")
