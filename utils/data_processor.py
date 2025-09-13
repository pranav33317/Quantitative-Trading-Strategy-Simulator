import pandas as pd
import numpy as np

def clean_data(data):
    """
    Clean and preprocess financial data
    """
    # Remove missing values
    data = data.dropna()
    
    # Remove duplicates
    data = data[~data.index.duplicated(keep='first')]
    
    # Ensure data is sorted by date
    data = data.sort_index()
    
    return data

def calculate_returns(data):
    """
    Calculate daily returns
    """
    data['returns'] = data['Close'].pct_change()
    return data

def calculate_technical_indicators(data, window_short=20, window_long=50):
    """
    Calculate technical indicators
    """
    # Moving averages
    data['sma_short'] = data['Close'].rolling(window=window_short).mean()
    data['sma_long'] = data['Close'].rolling(window=window_long).mean()
    
    # Bollinger Bands
    data['bb_middle'] = data['Close'].rolling(window=20).mean()
    bb_std = data['Close'].rolling(window=20).std()
    data['bb_upper'] = data['bb_middle'] + (bb_std * 2)
    data['bb_lower'] = data['bb_middle'] - (bb_std * 2)
    
    # RSI
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['rsi'] = 100 - (100 / (1 + rs))
    
    return data

def prepare_data(data, window_short=20, window_long=50):
    """
    Prepare data for backtesting
    """
    data = clean_data(data)
    data = calculate_returns(data)
    data = calculate_technical_indicators(data, window_short, window_long)
    return data
