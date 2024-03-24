import requests
import pandas as pd
from datetime import datetime, timedelta
import csv
import time


api_key = 'API_KEY'

rate_limit_delay = 0.5

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
trades_data = {'symbol': [], 'action': [], 'price': [], 'date': []}

# Backtesting logic
start_date = datetime.now() - timedelta(weeks=2)
end_date = datetime.now()

for symbol in symbols_df['symbol']:
    # Loop through each day in the date range
    current_date = start_date
    while current_date <= end_date:
        # Fetch data for the current date
        print(current_date)
        day_minute_data = get_intraday_data(symbol, api_key, current_date, current_date)
        
        if not day_minute_data.empty:
            if len(day_minute_data) >= 100:
                a_t = calculate_momentum_factor(day_minute_data['close'])
                if a_t is not None:
                    # Determine if price is ascending or descending
                    if a_t > 0.2:
                        trades_data['symbol'].append(symbol)
                        trades_data['action'].append('buy')
                        trades_data['price'].append(day_minute_data['close'].iloc[-1])
                        trades_data['date'].append(day_minute_data['date'].iloc[-1])
                        #print(f"{symbol} on {current_date.date()}: Price is ascending. Consider buying.")
                    elif a_t < -0.2:
                        trades_data['symbol'].append(symbol)
                        trades_data['action'].append('sell')
                        trades_data['price'].append(day_minute_data['close'].iloc[-1])
                        trades_data['date'].append(day_minute_data['date'].iloc[-1])
                        #print(f"{symbol} on {current_date.date()}: Price is descending. Consider selling.")
                #else:
                    #print(f"Not enough valid data to calculate momentum factor for {symbol} on {current_date.date()}")
            else:
                print(f"Not enough data points for momentum calculation for {symbol} on {current_date.date()}")
        else:
            print(f"No data returned for {symbol} on {current_date.date()}")
        
        # Move to the next day
        time.sleep(rate_limit_delay)
        
        current_date += timedelta(days=1)
# Convert the dictionary to a DataFrame
trades_df = pd.DataFrame(trades_data)

# Save the DataFrame to a CSV file
trades_df.to_csv("data/trades_data.csv", index=False)

print("Trades data CSV generated.")