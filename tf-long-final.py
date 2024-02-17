# Import pandas, yfinance, and os libraries
import pandas as pd
import yfinance as yf
import os
import time

import os
import shutil

def remove_directory_recursively(directory_path):
    try:
        shutil.rmtree(directory_path)
        print(f"Directory '{directory_path}' and its contents have been removed successfully.")
    except Exception as e:
        print(f"Error deleting directory: {e}")

if __name__ == "__main__":
    directories_to_remove = ["stocks-bse-output", "stocks-output"]
    for directory in directories_to_remove:
        remove_directory_recursively(directory)

# Get the script start time in the required format
start_time = time.strftime('%Y-%m-%d-%H-%M')

# Create a list of input files and a list of output folders
input_files = ['stocks.txt', 'stocks-bse.txt']
output_folders = ['stocks-output', 'stocks-bse-output']

# Define a function that takes an input file, an output folder, and returns a tuple of the data, the signals, and the stock name
def process_stock(input_file, output_folder):
    # Read the list of stocks from the input file
    stocks = pd.read_csv(input_file, header=None)
    stocks = stocks.squeeze()

    # Create an empty data frame to store the results
    results = pd.DataFrame(columns=['Stock', 'Daily', 'Weekly', 'Monthly', 'Weekly-Immediate', 'Monthly-Immediate'])

    # Create empty lists to store the stocks based on the signals
    daily_stocks = []
    weekly_stocks = []
    monthly_stocks = []
    weekly_immediate_stocks = []
    monthly_immediate_stocks = []

    # Create an empty list to store the failed symbols
    failed_stocks = []

    # Loop through each stock in the list
    for stock in stocks:
        try:
            # Download the historical data from Yahoo Finance
            data = yf.download(stock, period='3mo')
            
            # Calculate the daily condition
            daily_condition = (data['Close'].iloc[-1] > data['Open'].iloc[-3]) and (data['Open'].iloc[-3] > data['Close'].iloc[-3]) and (data['Open'].iloc[-2] < data['Close'].iloc[-2]) and (data['Close'].iloc[-1] > data['Open'].iloc[-1])
            # Assign the daily signal based on the condition
            daily_signal = 'TF-long' if daily_condition else 'no-signal'
            
            # Calculate the weekly condition
            weekly_condition = (data['Close'].resample('W').last().iloc[-1] > data['Open'].resample('W').first().iloc[-3]) and (data['Open'].resample('W').first().iloc[-3] > data['Close'].resample('W').last().iloc[-3]) and (data['Open'].resample('W').first().iloc[-2] < data['Close'].resample('W').last().iloc[-2]) and (data['Close'].resample('W').last().iloc[-1] > data['Open'].resample('W').first().iloc[-1])
            # Assign the weekly signal based on the condition
            weekly_signal = 'TF-long' if weekly_condition else 'no-signal'
            
            # Calculate the monthly condition
            monthly_condition = (data['Close'].resample('M').last().iloc[-1] > data['Open'].resample('M').first().iloc[-3]) and (data['Open'].resample('M').first().iloc[-3] > data['Close'].resample('M').last().iloc[-3]) and (data['Open'].resample('M').first().iloc[-2] < data['Close'].resample('M').last().iloc[-2]) and (data['Close'].resample('M').last().iloc[-1] > data['Open'].resample('M').first().iloc[-1])
            # Assign the monthly signal based on the condition
            monthly_signal = 'TF-long' if monthly_condition else 'no-signal'
            
            # Calculate the weekly-immediate condition
            weekly_immediate_condition = (data['Close'].resample('W').last().iloc[-1] > data['Open'].resample('W').first().iloc[-2]) and (data['Open'].resample('W').first().iloc[-2] > data['Close'].resample('W').last().iloc[-2])
            # Assign the weekly-immediate signal based on the condition
            weekly_immediate_signal = 'TF-long' if weekly_immediate_condition else 'no-signal'
            
            # Calculate the monthly-immediate condition
            monthly_immediate_condition = (data['Close'].resample('M').last().iloc[-1] > data['Open'].resample('M').first().iloc[-2]) and (data['Open'].resample('M').first().iloc[-2] > data['Close'].resample('M').last().iloc[-2])
            # Assign the monthly-immediate signal based on the condition
            monthly_immediate_signal = 'TF-long' if monthly_immediate_condition else 'no-signal'
            
            # Append the results to the data frame
            results = pd.concat([results, pd.DataFrame({'Stock': stock, 'Daily': daily_signal, 'Weekly': weekly_signal, 'Monthly': monthly_signal, 'Weekly-Immediate': weekly_immediate_signal, 'Monthly-Immediate': monthly_immediate_signal}, index=[0])], ignore_index=True)
            
            # Append the stock name to the lists based on the signals
            if daily_signal == 'TF-long':
                daily_stocks.append(stock)
            if weekly_signal == 'TF-long':
                weekly_stocks.append(stock)
            if monthly_signal == 'TF-long':
                monthly_stocks.append(stock)
            if weekly_immediate_signal == 'TF-long':
                weekly_immediate_stocks.append(stock)
            if monthly_immediate_signal == 'TF-long':
                monthly_immediate_stocks.append(stock)
            
            # Print the output for each iteration
            print(f'Daily TF-long signal: {daily_signal}')
            print(f'Weekly TF-long signal: {weekly_signal}')
            print(f'Monthly TF-long signal: {monthly_signal}')
            print(f'Weekly-immediate TF-long signal: {weekly_immediate_signal}')
            print(f'Monthly-immediate TF-long signal: {monthly_immediate_signal}')
            print(f'Stock name: {stock}')
            print()
        except IndexError:
            # Skip the symbol that causes the error and print a message
            print(f'Skipping {stock} due to insufficient data')
            # Add the symbol to the failed list
            failed_stocks.append(stock)
            continue

    # Create the output folder in the current working directory using the output folder name
    os.mkdir(output_folder)

    # Write the lists to different text files in the output folder
    with open(os.path.join(output_folder, 'daily_stocks.txt'), 'w') as f:
        for stock in daily_stocks:
            f.write(stock + '\n')

    with open(os.path.join(output_folder, 'weekly_stocks.txt'), 'w') as f:
        for stock in weekly_stocks:
            f.write(stock + '\n')

    with open(os.path.join(output_folder, 'monthly_stocks.txt'), 'w') as f:
        for stock in monthly_stocks:
            f.write(stock + '\n')

    with open(os.path.join(output_folder, 'weekly_immediate_stocks.txt'), 'w') as f:
        for stock in weekly_immediate_stocks:
            f.write(stock + '\n')

    with open(os.path.join(output_folder, 'monthly_immediate_stocks.txt'), 'w') as f:
        for stock in monthly_immediate_stocks:
            f.write(stock + '\n')

    # Write the failed list to a file named as failed_stocks.txt in the output folder
    with open(os.path.join(output_folder, 'failed_stocks.txt'), 'w') as f:
        for stock in failed_stocks:
            f.write(stock + '\n')

    # Save the results to a single file named as results.csv in the output folder
    results.to_csv(os.path.join(output_folder, 'results.csv'), index=False)

# Loop through the input files and output folders in parallel
for input_file, output_folder in zip(input_files, output_folders):
    # Call the process_stock function for each input file and output folder
    process_stock(input_file, output_folder)
