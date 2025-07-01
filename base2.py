import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Configurar la app
st.set_page_config(page_title="Dashboard Psicológico", layout="wide")

# Cargar y limpiar datos
@st.cache_data
def cargar_datos():
    df = pd.read_csv("Copia de ejercicio analisis de datos.csv")
    # Normalizar nombres de columnas: quitar espacios, pasar a minúsculas, reemplazar acentos
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )
    return df

df = cargar_datos()

# Mostrar las columnas disponibles (para depurar si hay errores)
st.sidebar.write("🧾 Columnas disponibles:")
st.sidebar.write(df.columns.tolist())

# Título de la app
st.title("Dashboard de análisis psicológico")

# Mostrar tabla si el usuario quiere
if st.checkbox("Mostrar los primeros datos"):
    st.dataframe(df.head())

# Filtro por género
if "genero" in df.columns:
    generos = df['genero'].dropna().unique().tolist()
    genero_seleccionado = st.radio("Filtrar por género", options=["Todos"] + generos)
    if genero_seleccionado != "Todos":
        df_filtrado = df[df["genero"] == genero_seleccionado]
    else:
        df_filtrado = df
else:
    st.warning("No se encontró la columna 'genero'.")
    df_filtrado = df

# Función para mostrar mapa de calor
def mostrar_heatmap(data, x_col, y_col, title):
    if x_col not in data.columns or y_col not in data.columns:
        st.warning(f"No se encuentran las columnas '{x_col}' y/o '{y_col}'.")
        return
    pivot = data.pivot_table(index=y_col, columns=x_col, aggfunc='size', fill_value=0)
    fig, ax = plt.subplots()
    sns.heatmap(pivot, cmap="YlGnBu", annot=True, fmt="d", ax=ax)
    ax.set_title(title)
    st.pyplot(fig)

# Mostrar mapas de calor
col1, col2 = st.columns(2)

with col1:
    st.subheader("Hora de despertar vs Dificultad para recordar")
    mostrar_heatmap(df_filtrado, "hora_de_despertar", "dificultad_recordar", "Despertar vs Recordar")

with col2:
    st.subheader("Frecuencia de ansiedad vs Frecuencia de depresión")
    mostrar_heatmap(df_filtrado, "frecuencia_ansiedad", "frecuecia_depresion", "Ansiedad vs Depresión")
