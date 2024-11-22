import pandas as pd
import streamlit as st
from PIL import Image

# Título de la aplicación
st.title('Análisis de datos de Sensores en Mi Ciudad')
image = Image.open('grafana2.jpg')
st.image(image)

# Subir archivo
uploaded_file = st.file_uploader('Elige un archivo CSV')

if uploaded_file is not None:
    df1 = pd.read_csv(uploaded_file)
    
    st.subheader('Perfil gráfico de la variable medida.')
    # Asegurar que la columna 'Time' esté como índice si existe
    if 'Time' in df1.columns:
        df1['Time'] = pd.to_datetime(df1['Time'])
        df1 = df1.set_index('Time')
    
    st.line_chart(df1)
    st.write(df1)
    
    st.subheader('Estadísticos básicos de los sensores.')
    st.dataframe(df1["temperatura ESP32"].describe())
    
    # Cálculo del índice de confort térmico
    st.subheader('Cálculo del Índice de Confort Térmico')
    
    def calcular_sensacion_termica(temp, hum):
        # Fórmula del índice de calor de Steadman (simplificada)
        st_index = (
            -8.78469475556
            + 1.61139411 * temp
            + 2.33854883889 * hum
            - 0.14611605 * temp * hum
            - 0.012308094 * (temp**2)
            - 0.0164248277778 * (hum**2)
            + 0.002211732 * (temp**2) * hum
            + 0.00072546 * temp * (hum**2)
            - 0.000003582 * (temp**2) * (hum**2)
        )
        return st_index

    # Verificar que existen las columnas necesarias
    if "temperatura ESP32" in df1.columns and "humedad ESP32" in df1.columns:
        # Manejar valores faltantes
        df1 = df1.dropna(subset=["temperatura ESP32", "humedad ESP32"])
        
        # Calcular la sensación térmica
        df1["Sensación Térmica"] = df1.apply(
            lambda row: calcular_sensacion_termica(row["temperatura ESP32"], row["humedad ESP32"]), axis=1
        )
        
        # Verificar si la columna fue añadida correctamente
        st.write("Datos con Sensación Térmica incluida:")
        st.write(df1)
        
        # Visualización de la sensación térmica
        st.subheader('Gráfico de Sensación Térmica')
        st.line_chart(df1["Sensación Térmica"])
    else:
        st.error("El archivo debe incluir las columnas 'temperatura ESP32' y 'humedad ESP32'.")
    
    # Filtrar por temperatura mínima
    min_temp = st.slider('Selecciona la temperatura mínima (°C)', min_value=-10, max_value=45, value=23, key=1)
    filtrado_df_min = df1.query(f"`temperatura ESP32` > {min_temp}")
    st.subheader("Temperaturas superiores al valor configurado.")
    st.write(filtrado_df_min)

    # Filtrar por temperatura máxima
    max_temp = st.slider('Selecciona la temperatura máxima (°C)', min_value=-10, max_value=45, value=30, key=2)
    filtrado_df_max = df1.query(f"`temperatura ESP32` < {max_temp}")
    st.subheader("Temperaturas inferiores al valor configurado.")
    st.write(filtrado_df_max)

else:
    # Aquí es donde el bloque else debía manejarse correctamente
    st.warning('Necesitas cargar un archivo CSV.')


