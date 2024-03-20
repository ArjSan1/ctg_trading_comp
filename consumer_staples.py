import requests
from bs4 import BeautifulSoup
import pandas as pd
# Function to scrape Consumer Staples stocks from StockAnalysis
def scrape_consumer_staples(url):
    response = requests.get(url)
    stocks = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        main_table = soup.find('table', id='main-table')
        if main_table:
            for row in main_table.find_all('tr')[1:]:  # Skip the header row
                cells = row.find_all('td')
                if len(cells) > 1:  # Making sure there's enough cells
                    stock_symbol = cells[1].text  # Assuming second cell contains the symbol
                    stocks.append(stock_symbol.strip())  # Strip to remove extra whitespace
                    
    else:
        print(f"Failed to scrape Consumer Staples stocks: {response.status_code}")
    return stocks

# Example usage
url = "https://stockanalysis.com/stocks/sector/consumer-staples/"
consumer_staples_symbols = scrape_consumer_staples(url)
print(type(consumer_staples_symbols))
df = pd.DataFrame(consumer_staples_symbols)
df.to_csv('data/consumer_staples.csv')
