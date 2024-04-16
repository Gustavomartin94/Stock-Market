import requests
import pandas as pd
from datetime import datetime
from config import KEY

# Reemplaza 'YOUR_API_KEY' con tu propio código de API de AlphaVantage
API_KEY = KEY

# Lista de símbolos de acciones que deseas obtener datos
symbols = ['AAPL', 'GOOGL', 'MSFT']

# Lista para almacenar los DataFrames individuales de cada acción
dfs = []

for symbol in symbols:
    # URL de la API de AlphaVantage para obtener datos de acciones
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}'

    # Realiza la solicitud GET a la API
    response = requests.get(url)

    # Verifica si la solicitud fue exitosa
    if response.status_code == 200:
        data = response.json()['Time Series (Daily)']
        # Convertir el objeto JSON a un DataFrame de pandas
        df = pd.DataFrame.from_dict(data, orient='index')
        # Cambiar el nombre de las columnas
        df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        # Convertir los valores a tipos numéricos
        df = df.apply(pd.to_numeric)
        
        # Agregar la columna de Símbolo de la acción
        df['Symbol'] = symbol
        
        # Agregar la columna de Fecha_Actualizacion
        df['Fecha_Actualizacion'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Agregar la columna de Fecha
        df['Fecha'] = df.index
        
        # Agregar una columna de clave primaria e indice
        df['Primary_Key'] = df['Symbol'] + ' ' + df.index
        
        # Reordenar las columnas
        df = df[['Fecha', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Volume', 'Fecha_Actualizacion', 'Primary_Key']]
        
        # Agregar el DataFrame de esta acción a la lista
        dfs.append(df)
        
    else:
        print(f"Error al obtener datos para {symbol}: {response.status_code}")

# Combinar todos los DataFrames en uno solo
combined_df = pd.concat(dfs)

# Mostrar el DataFrame combinado
combined_df