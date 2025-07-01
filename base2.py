import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard Salud Mental", layout="centered")

st.title("📊 Dashboard de Análisis de Datos")
st.subheader("Relaciones entre variables categóricas")

# --- URL del archivo CSV desde GitHub ---
url_csv = st.text_input(
    "🔗 Pega aquí el enlace RAW de tu archivo CSV en GitHub:",
    placeholder="https://raw.githubusercontent.com/tu_usuario/tu_repo/main/Copia%20de%20ejercicio%20analisis%20de%20datos.csv"
)

if url_csv:
    try:
        df = pd.read_csv(url_csv)

        # Mapeo para claridad visual
        if 'dificultad_recordar' in df.columns:
            df['dificultad_recordar'] = df['dificultad_recordar'].map({0: 'No', 1: 'Sí'})

        # Filtro por género (si existe la columna)
        if 'genero' in df.columns:
            generos_disponibles = df['genero'].dropna().unique().tolist()
            filtro_genero = st.selectbox("Selecciona un género para filtrar:", ["Todos"] + generos_disponibles)
            df_filtrado = df[df['genero'] == filtro_genero] if filtro_genero != "Todos" else df
        else:
            df_filtrado = df
            st.warning("La columna 'genero' no fue encontrada. Se usará toda la muestra.")

        st.write(f"Mostrando **{len(df_filtrado)}** registros.")

        # --- MAPA DE CALOR 1 ---
        if 'hora_de_despertar' in df.columns and 'dificultad_recordar' in df.columns:
            st.markdown("### 🔥 Mapa de calor: Hora de despertar vs Dificultad para recordar")
            tabla1 = pd.crosstab(df_filtrado['hora_de_despertar'], df_filtrado['dificultad_recordar'])

            fig1, ax1 = plt.subplots()
            sns.heatmap(tabla1, annot=True, cmap="YlOrRd", fmt='d', ax=ax1)
            plt.xlabel("Dificultad para recordar")
            plt.ylabel("Hora de despertar")
            st.pyplot(fig1)
        else:
            st.error("Faltan columnas para el primer heatmap.")

        # --- MAPA DE CALOR 2 ---
        if 'frecuencia_ansiedad' in df.columns and 'frecuecia_depresion' in df.columns:
            st.markdown("### 🔥 Mapa de calor: Frecuencia de ansiedad vs Frecuencia de depresión")
            tabla2 = pd.crosstab(df_filtrado['frecuencia_ansiedad'], df_filtrado['frecuecia_depresion'])

            fig2, ax2 = plt.subplots()
            sns.heatmap(tabla2, annot=True, cmap="Blues", fmt='d', ax=ax2)
            plt.xlabel("Frecuencia de depresión")
            plt.ylabel("Frecuencia de ansiedad")
            st.pyplot(fig2)
        else:
            st.error("Faltan columnas para el segundo heatmap.")

    except Exception as e:
        st.error(f"❌ Error al cargar el archivo: {e}")

st.caption("Dashboard creado por Laura 🧠")
