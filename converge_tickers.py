import requests
import pandas as pd
from datetime import datetime, timedelta

# Insert your API key here
api_key = 'API_KEY'

# Define the period for the backtest to be the past two weeks
end_date = datetime.now()
start_date = end_date - timedelta(weeks=2)

# Load the list of consumer staple stocks from the provided CSV
consumer_staples_csv = pd.read_csv('data/consumer_staples.csv')

# Filter out the first column which seems to contain row indices
consumer_staples_symbols = consumer_staples_csv.iloc[:, 1].tolist()

# Function to get the full stock list from the API
def get_stocks_from_api(api_key):
    url = f"https://financialmodelingprep.com/api/v3/stock/list?apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        all_stocks = pd.DataFrame(response.json())
        return all_stocks
    else:
        print("Failed to fetch stock list:", response.status_code)
        return pd.DataFrame()

# Function to cross-check the symbols from the CSV with the stocks from the API
def cross_check_stocks(api_stocks_df, csv_stocks_list):
    # Use `.isin` to filter the dataframe for the symbols in the csv list
    return api_stocks_df[api_stocks_df['symbol'].isin(csv_stocks_list)]

# Fetch all stocks from the API
all_stocks_from_api = get_stocks_from_api(api_key)

# Perform the cross-check
cross_checked_stocks = cross_check_stocks(all_stocks_from_api, consumer_staples_symbols)

# Output the result
# print(type(cross_checked_stocks.head()))  # For now, just display the head of the dataframe

cross_checked_stocks.to_csv("data/consumer_staple_data.csv")