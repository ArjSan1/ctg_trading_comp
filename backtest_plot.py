import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()  # For datetime conversion for matplotlib

# Load the trades DataFrame
trades_df = pd.read_csv("data/trades_data.csv")
trades_df['date'] = pd.to_datetime(trades_df['date'])
trades_df.sort_values('date', inplace=True)  # Ensure the trades are sorted by date

# Starting capital
initial_capital = 10000
capital = initial_capital
holdings = {}

# Track capital over time
capital_over_time = [initial_capital]
dates = [trades_df['date'].min() - pd.Timedelta(days=1)]  # Start from the day before the first trade

# Process each trade in the DataFrame
for index, trade in trades_df.iterrows():
    symbol = trade['symbol']
    action = trade['action']
    price = trade['price']
    date = trade['date']
    
    if action == 'buy' and capital >= price:
        # Buy one unit
        capital -= price
        holdings[symbol] = holdings.get(symbol, 0) + 1
    elif action == 'sell' and holdings.get(symbol, 0) > 0:
        # Sell one unit
        capital += price
        holdings[symbol] -= 1
    
    # Record capital and date
    capital_over_time.append(capital)
    dates.append(date)

# If any holdings remain, sell them at the last known price
for symbol, count in holdings.items():
    if count > 0:
        last_price = trades_df[trades_df['symbol'] == symbol].iloc[-1]['price']
        capital += last_price * count
        holdings[symbol] = 0
        capital_over_time.append(capital)
        dates.append(trades_df['date'].iloc[-1])

# Plotting the capital over time
plt.figure(figsize=(14, 7))
plt.plot(dates, capital_over_time, marker='o')
plt.title('Strategy Capital Over Time')
plt.xlabel('Date')
plt.ylabel('Capital')
plt.xticks(rotation=45)  # Rotate the x-axis labels for better readability
plt.tight_layout()  # Adjust layout so all labels are visible
plt.grid(True)
plt.show()

# Final capital after selling all holdings
final_capital = capital

print(f"Initial Capital: {initial_capital}")
print(f"Final Capital after two weeks: {final_capital}")
