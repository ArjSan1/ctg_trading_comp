import matplotlib.pyplot as plt
import pandas as pd
# Simulated trades DataFrame
trades_df = pd.read_csv("data/trades_data")

# Starting capital
initial_capital = 10000
capital = initial_capital
holdings = {}

# Track capital over time
capital_over_time = []
dates = []

# Process each trade in the DataFrame
for index, trade in trades_df.iterrows():
    symbol = trade['symbol']
    action = trade['action']
    price = trade['price']
    date = trade['date']
    
    if action == 'buy':
        capital -= price  # Subtract the price from capital to buy
        if symbol in holdings:
            holdings[symbol] += 1  # Increase holdings for the symbol
        else:
            holdings[symbol] = 1  # Or set holdings to 1 if it's a new symbol
    elif action == 'sell':
        if symbol in holdings and holdings[symbol] > 0:
            capital += price  # Add the price to capital to sell
            holdings[symbol] -= 1  # Decrease holdings for the symbol
    
    # Record capital and date
    capital_over_time.append(capital)
    dates.append(date)

# Assume that we close out all positions at the last known price for each symbol
for symbol in holdings:
    if holdings[symbol] > 0:
        # Get the last known price for the symbol from the trades
        last_price = trades_df[trades_df['symbol'] == symbol]['price'].iloc[-1]
        capital += holdings[symbol] * last_price
        holdings[symbol] = 0

# Plotting the capital over time
plt.figure(figsize=(10, 5))
plt.plot(dates, capital_over_time, marker='o')
plt.title('Strategy Capital Over Time')
plt.xlabel('Date')
plt.ylabel('Capital')
plt.grid(True)
plt.show()

# Final capital after selling all holdings
final_capital = capital

print(f"Initial Capital: {initial_capital}")
print(f"Final Capital after two weeks: {final_capital}")