import requests
import pandas as pd
from datetime import datetime, timedelta
import csv

api_key = '4ff69fe86648f6d763ff545f15bb38b4'


symbols_df = pd.read_csv("data/consumer_staple_data.csv")
#print(symbols_df.head)
# Function to get minute-by-minute data
def get_intraday_data(symbol, api_key, start_date, end_date):
    # Convert datetime objects to strings in the format required by the API
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    
    # API endpoint for 1-minute interval intraday data
    url = f"https://financialmodelingprep.com/api/v3/historical-chart/1min/{symbol}?from={start_date_str}&to={end_date_str}&apikey={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data:  # Check if data is not empty
            # Create DataFrame and ensure 'date' column is present
            df = pd.DataFrame(data)
            if 'date' in df.columns:
                return df
            else:
                print(f"Date column missing in the data for {symbol}")
                return pd.DataFrame()
        else:
            print(f"No data returned from the API for {symbol}")
            return pd.DataFrame()
    else:
        print(f"Failed to fetch data for {symbol}: Status Code {response.status_code}")
        return pd.DataFrame()

# Function to calculate the momentum factor a_t
def calculate_momentum_factor(price_series):
    if len(price_series) < 101:
        # We need at least 101 prices to calculate 100 differences
        return None

    # Calculate the absolute price differences for 100 minutes
    abs_diff = price_series.diff().abs().iloc[-100:]
    
    # Calculate the price differences without taking the absolute value
    plain_diff = price_series.diff().iloc[-100:]
    
    # Calculate numerator and denominator separately according to the formula
    numerator = abs_diff.sum()
    denominator = plain_diff.sum()

    # In case denominator is zero, avoid division by zero
    if denominator == 0:
        return None
    
    # Calculate a_t
    a_t = numerator / denominator
    
    return a_t
# Backtesting logic
start_date = datetime.now() - timedelta(weeks=2)
end_date = datetime.now()

for symbol in symbols_df['symbol']:
    # Fetch minute-by-minute data for the past two weeks
    minute_data = get_intraday_data(symbol, api_key, start_date, end_date)
    
    if not minute_data.empty:
        # Check if we have at least 100 data points to calculate the momentum factor
        if len(minute_data) >= 100:
            print(f"{len(minute_data)} {symbol}")
            # Calculate a_t for the latest minute
            a_t = calculate_momentum_factor(minute_data['close'])
            if a_t is not None:  # Ensure a_t was calculated
                # Determine if price is ascending or descending
                print(f"{a_t}")
                if a_t > 0.2:
                    print(f"{symbol}: Price is ascending. Consider buying.")
                elif a_t < -0.2:
                    print(f"{symbol}: Price is descending. Consider selling.")
            else:
                 print(f"Not enough valid data to calculate momentum factor for {symbol} {a_t}")
        else:
            print(f"Not enough data points for momentum calculation for {symbol}")
    else:
        print(f"No data returned for {symbol}")