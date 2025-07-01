import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Configuración inicial
st.set_page_config(page_title="Dashboard Psicológico", layout="wide")

# URL del archivo CSV en GitHub (RAW)
url = "https://raw.githubusercontent.com/tu_usuario/tu_repo/main/Copia%20de%20ejercicio%20analisis%20de%20datos.csv"

# Carga de datos
@st.cache_data
def cargar_datos():
    df = pd.read_csv(url)
    return df

df = cargar_datos()

# Título
st.title("Dashboard de análisis psicológico")

# Mostrar los primeros datos
if st.checkbox("Mostrar datos"):
    st.dataframe(df.head())

# Filtro por género
generos = df['genero'].dropna().unique().tolist()
genero_seleccionado = st.radio("Filtrar por género", options=["Todos"] + generos)

# Aplicar filtro si se selecciona género
if genero_seleccionado != "Todos":
    df_filtrado = df[df["genero"] == genero_seleccionado]
else:
    df_filtrado = df

# Función para graficar mapa de calor
def mostrar_heatmap(data, x_col, y_col, title):
    pivot_table = data.pivot_table(index=y_col, columns=x_col, aggfunc='size', fill_value=0)
    fig, ax = plt.subplots()
    sns.heatmap(pivot_table, cmap="YlGnBu", annot=True, fmt="d", ax=ax)
    ax.set_title(title)
    st.pyplot(fig)

# Layout en dos columnas
col1, col2 = st.columns(2)

with col1:
    st.subheader("Hora de despertar vs Dificultad para recordar")
    mostrar_heatmap(df_filtrado, "hora_de_despertar", "dificultad_recordar", "Mapa de calor: despertar vs recordar")

with col2:
    st.subheader("Frecuencia de ansiedad vs Depresión")
    mostrar_heatmap(df_filtrado, "frecuencia_ansiedad", "frecuencia_depresion", "Mapa de calor: ansiedad vs depresión")
