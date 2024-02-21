# Import pandas and yfinance libraries
import pandas as pd
import yfinance as yf

# Define the number of days to look back
days = 2

# Define the end date as today
end_date = pd.to_datetime("today")

# Define the start date as days ago
start_date = end_date - pd.Timedelta(days=days)

# Create an empty list to store the results
results = []

# Open the stocks.txt file and read the stock symbols
with open("stocks.txt", "r") as f:
    stocks = f.read().splitlines()

# Loop through each stock symbol
for stock in stocks:
    # Fetch the historical data from yfinance
    data = yf.download(stock, start=start_date, end=end_date)
    # Get the open price of the start date
    open_price = data["Open"].iloc[0]
    # Get the close price of the end date
    close_price = data["Close"].iloc[-1]
    # Calculate the difference
    difference = close_price - open_price
    # Calculate the percentage change
    percentage_change = (difference / open_price) * 100
    # Append the result to the list
    results.append([stock, open_price, close_price, difference, percentage_change])

# Create a pandas dataframe from the results
df = pd.DataFrame(results, columns=["Stock", "Open", "Close", "Difference", "Percentage Change"])

# Save the dataframe as a csv file
df.to_csv("stock_difference.csv", index=False)

# Print the dataframe to the standard output
print(df)

# Print a message
print("The script has finished running and the csv file has been saved.")
