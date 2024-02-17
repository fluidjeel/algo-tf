# Import pandas and yfinance libraries
import pandas as pd
import yfinance as yf

# Read the list of stocks from the file stocks-bse.txt
stocks = pd.read_csv('stocks-bse.txt', header=None)
stocks = stocks.squeeze()

# Create empty lists to store the valid and missing stocks
valid_stocks = []
missing_stocks = []

# Loop through each stock in the list
for stock in stocks:
    # Download the historical data from Yahoo Finance for the last 3 months
    data = yf.download(stock, period='3mo')
    # Check if the data is empty
    if data.empty:
        # Add the stock to the missing list
        missing_stocks.append(stock)
    else:
        # Add the stock to the valid list
        valid_stocks.append(stock)

# Write the valid list to the file stocks-bse.txt
with open('stocks-bse.txt', 'w') as f:
    for stock in valid_stocks:
        f.write(stock + '\n')

# Write the missing list to the file stocks-missing.txt
with open('stocks-missing.txt', 'w') as f:
    for stock in missing_stocks:
        f.write(stock + '\n')
