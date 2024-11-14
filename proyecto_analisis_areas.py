import requests
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# 1. Cargar los datos desde la API pública
url = 'https://datos.gob.cl/api/3/action/datastore_search?resource_id=fe256fe6-e1d5-4eea-b98b-1147f4a05809&limit=100'
response = requests.get(url)  # Obtener los datos de la API
data = response.json()  # Convertir la respuesta en formato JSON

# 2. Crear DataFrame con pandas
datos = pd.DataFrame(data['result']['records'])

# 3. Limpiar los datos, renombrar las columnas y convertir los valores de los años en numéricos
datos = datos.dropna(how='all')  # Eliminar filas completamente vacías
datos.columns = ['_id', 'AREA / AÑOS', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011']

# Convertir las columnas de los años a tipo numérico (para permitir análisis)
for col in ['2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011']:
    datos[col] = pd.to_numeric(datos[col], errors='coerce')

# Eliminar filas con valores nulos en el nombre del área
datos = datos[datos['AREA / AÑOS'].notna()]

# 4. Interfaz con Streamlit
st.title('Evolución de las Áreas a lo largo de los Años')
area = st.selectbox('Selecciona el área', datos['AREA / AÑOS'].unique())

# Filtrar los datos según el área seleccionada
area_data = datos[datos['AREA / AÑOS'] == area]

# 5. Generar el gráfico de línea
fig, ax = plt.subplots()
ax.plot(area_data.columns[2:], area_data.iloc[0, 2:], marker='o', linestyle='-', color='b')
ax.set_title(f'Evolución de {area}')
ax.set_xlabel('Año')
ax.set_ylabel('Cantidad')

# 6. Mostrar el gráfico en la interfaz web
st.pyplot(fig)
