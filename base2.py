import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Configuración de la app
st.set_page_config(page_title="Dashboard Psicológico", layout="wide")

# Cargar archivo local
@st.cache_data
def cargar_datos():
    df = pd.read_csv("Copia de ejercicio analisis de datos.csv")
    return df

df = cargar_datos()

# Título de la app
st.title("Dashboard de análisis psicológico")

# Mostrar datos si el usuario quiere
if st.checkbox("Mostrar datos"):
    st.dataframe(df.head())

# Filtro por género
generos = df['genero'].dropna().unique().tolist()
genero_seleccionado = st.radio("Filtrar por género", options=["Todos"] + generos)

# Aplicar filtro
if genero_seleccionado != "Todos":
    df_filtrado = df[df["genero"] == genero_seleccionado]
else:
    df_filtrado = df

# Función para mostrar mapa de calor
def mostrar_heatmap(data, x_col, y_col, title):
    pivot = data.pivot_table(index=y_col, columns=x_col, aggfunc='size', fill_value=0)
    fig, ax = plt.subplots()
    sns.heatmap(pivot, cmap="YlGnBu", annot=True, fmt="d", ax=ax)
    ax.set_title(title)
    st.pyplot(fig)

# Mostrar los dos mapas de calor en columnas
col1, col2 = st.columns(2)

with col1:
    st.subheader("Hora de despertar vs Dificultad para recordar")
    mostrar_heatmap(df_filtrado, "hora_de_despertar", "dificultad_recordar", "Despertar vs Recordar")

with col2:
    st.subheader("Frecuencia de ansiedad vs Frecuencia de depresión")
    mostrar_heatmap(df_filtrado, "frecuencia_ansiedad", "frecuencia_depresion", "Ansiedad vs Depresión")
