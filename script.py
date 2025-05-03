import requests
import pandas as pd
from datetime import datetime
from config import KEY

# Replace 'YOUR_API_KEY' with your own AlphaVantage API key
API_KEY = KEY

# List of stock symbols you want to retrieve data for
symbols = ['AAPL', 'GOOGL', 'MSFT']

# List to store individual DataFrames for each stock
dfs = []

for symbol in symbols:
    # AlphaVantage API URL to get stock data
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}'

    # Make a GET request to the API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()['Time Series (Daily)']
        # Convert the JSON object to a Pandas DataFrame
        df = pd.DataFrame.from_dict(data, orient='index')
        # Rename the columns
        df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        # Convert values to numeric types
        df = df.apply(pd.to_numeric)
        
        # Add the stock symbol column
        df['Symbol'] = symbol
        
        # Add the update date column
        df['Fecha_Actualizacion'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Add the date column
        df['Fecha'] = df.index
        
        # Add a primary key and index column
        df['Primary_Key'] = df['Symbol'] + ' ' + df.index
        
        # Reorder the columns
        df = df[['Fecha', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Volume', 'Fecha_Actualizacion', 'Primary_Key']]
        
        # Add the DataFrame for this stock to the list
        dfs.append(df)
        
    else:
        print(f"Error retrieving data for {symbol}: {response.status_code}")

# Combine all DataFrames into a single one
combined_df = pd.concat(dfs)

# Display the combined DataFrame
combined_df