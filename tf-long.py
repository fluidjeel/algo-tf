# Import pandas, yfinance and csv libraries
import pandas as pd
import yfinance as yf
import csv

# Define a function to scan the stock data for a given timeframe
def scan_stock(stock, timeframe):
  # Check the timeframe and set the start and end date accordingly
  if timeframe == 'daily':
    # Use the last 3 days of data
    end = pd.to_datetime ('today')
    start = end - pd.Timedelta (days=3)
  elif timeframe == 'weekly':
    # Use the last 3 weeks of data
    end = pd.to_datetime ('today') - pd.offsets.Week (weekday=4) # Friday
    start = end - pd.offsets.Week (n=3)
  elif timeframe == 'monthly':
    # Use the last 3 months of data
    end = pd.to_datetime ('today') - pd.offsets.MonthEnd (n=1) # Last day of previous month
    start = end - pd.offsets.MonthBegin (n=3)
  else:
    # Invalid timeframe
    return None
  
  # Download the stock data from yahoo finance
  data = yf.download(stock, start, end)
  # Resample the data based on the timeframe
  data = data.resample (timeframe[0].upper ()).agg ({'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum'})
  # Create a new column for the previous period's close
  data['PrevClose'] = data['Close'].shift(1)
  # Create a new column for the previous period's open
  data['PrevOpen'] = data['Open'].shift(1)
  # Create a new column for the period before previous period's close
  data['PrevPrevClose'] = data['Close'].shift(2)
  # Create a new column for the period before previous period's open
  data['PrevPrevOpen'] = data['Open'].shift(2)
  # Create a new column for the first condition
  data['Condition1'] = (data['PrevPrevClose'] < data['PrevPrevOpen'])
  # Create a new column for the second condition
  data['Condition2'] = (data['PrevClose'] > data['PrevOpen']) & (data['Open'] < data['Close']) & (data['Close'] > data['PrevOpen'])
  # Create a new column for the third condition
  data['Condition3'] = (data['Close'] > data['PrevPrevOpen'])
  # Create a new column for the result
  data['Result'] = data.apply(lambda row: 'TF-long' if row['Condition1'] and row['Condition2'] and row['Condition3'] else 'no signal', axis=1)
  # Return the last result
  return data['Result'].iloc [-1]

# Define the input and output files
input_file = 'stocks.txt'
output_file = 'results.csv'

# Define the timeframes
timeframes = ['daily', 'weekly', 'monthly']

# Ask the user to enter the desired timeframe
timeframe = input("Enter the timeframe: ")

# Check if the timeframe is valid
if timeframe not in timeframes and timeframe != 'all':
  # Invalid timeframe
  print("Invalid timeframe. Please enter one of the following: daily, weekly, monthly, or all.")
else:
  # Open the input file and read the stock symbols
  with open (input_file, 'r') as infile:
    stocks = infile.read().splitlines()

  # Open the output file and write the results
  with open (output_file, 'w', newline='') as outfile:
    writer = csv.writer (outfile)
    # Write the header row
    if timeframe == 'all':
      # Write all the timeframes
      writer.writerow (['Stock', 'Daily', 'Weekly', 'Monthly'])
    else:
      # Write only the selected timeframe
      writer.writerow (['Stock', timeframe.capitalize()])
    # Loop through the stocks
    for stock in stocks:
      # Get the stock symbol
      symbol = stock
      # Create an empty list to store the results
      results = [symbol]
      # Check if the user wants all the timeframes
      if timeframe == 'all':
        # Loop through all the timeframes
        for tf in timeframes:
          # Scan the stock data for the given timeframe
          result = scan_stock (symbol, tf)
          # Append the result to the list
          results.append (result)
      else:
        # Scan the stock data for the selected timeframe
        result = scan_stock (symbol, timeframe)
        # Append the result to the list
        results.append (result)
      # Write the results to the output file
      writer.writerow (results)
