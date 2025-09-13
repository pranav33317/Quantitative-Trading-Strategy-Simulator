import pandas as pd
import yfinance as yf
from alpha_vantage.timeseries import TimeSeries
import os
import time

def fetch_yahoo_data(ticker, start_date, end_date, interval='1d'):
    """
    Fetch historical data from Yahoo Finance
    """
    try:
        data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
        return data
    except Exception as e:
        print(f"Error fetching data from Yahoo Finance: {e}")
        return None

def fetch_alpha_vantage_data(api_key, ticker, output_size='compact'):
    """
    Fetch historical data from Alpha Vantage
    """
    try:
        ts = TimeSeries(key=api_key, output_format='pandas')
        data, meta_data = ts.get_daily(symbol=ticker, outputsize=output_size)
        return data
    except Exception as e:
        print(f"Error fetching data from Alpha Vantage: {e}")
        return None

def save_data(data, filename, directory):
    """
    Save data to CSV file
    """
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, filename)
    data.to_csv(filepath)
    print(f"Data saved to {filepath}")

def load_data(filename, directory):
    """
    Load data from CSV file
    """
    filepath = os.path.join(directory, filename)
    if os.path.exists(filepath):
        return pd.read_csv(filepath, index_col=0, parse_dates=True)
    else:
        print(f"File {filepath} does not exist")
        return None
