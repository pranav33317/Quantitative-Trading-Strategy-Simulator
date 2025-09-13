import pandas as pd
import numpy as np

class Backtester:
    def __init__(self, initial_capital=10000.0):
        self.initial_capital = initial_capital
        self.positions = pd.DataFrame()
        self.portfolio = pd.DataFrame()
        
    def run_backtest(self, data, signals):
        """
        Run backtest on the strategy
        """
        # Initialize portfolio
        portfolio = pd.DataFrame(index=signals.index)
        portfolio['price'] = data['Close']
        portfolio['cash'] = self.initial_capital
        portfolio['holdings'] = 0
        portfolio['total'] = self.initial_capital
        portfolio['returns'] = 0.0
        
        # Track positions
        positions = pd.DataFrame(index=signals.index)
        positions['positions'] = signals['positions']
        
        # Execute backtest
        for i in range(1, len(portfolio)):
            current_date = portfolio.index[i]
            previous_date = portfolio.index[i-1]
            
            # Update cash position from previous day
            portfolio.loc[current_date, 'cash'] = portfolio.loc[previous_date, 'cash']
            
            # Check for buy signal
            if positions.loc[current_date, 'positions'] > 0:
                # Buy as many shares as possible
                shares_to_buy = portfolio.loc[current_date, 'cash'] // portfolio.loc[current_date, 'price']
                portfolio.loc[current_date, 'holdings'] = portfolio.loc[previous_date, 'holdings'] + shares_to_buy
                portfolio.loc[current_date, 'cash'] -= shares_to_buy * portfolio.loc[current_date, 'price']
            
            # Check for sell signal
            elif positions.loc[current_date, 'positions'] < 0:
                # Sell all shares
                portfolio.loc[current_date, 'cash'] += portfolio.loc[previous_date, 'holdings'] * portfolio.loc[current_date, 'price']
                portfolio.loc[current_date, 'holdings'] = 0
            
            # No signal, maintain position
            else:
                portfolio.loc[current_date, 'holdings'] = portfolio.loc[previous_date, 'holdings']
            
            # Update total portfolio value
            portfolio.loc[current_date, 'total'] = (
                portfolio.loc[current_date, 'cash'] + 
                portfolio.loc[current_date, 'holdings'] * portfolio.loc[current_date, 'price']
            )
            
            # Calculate daily returns
            portfolio.loc[current_date, 'returns'] = (
                portfolio.loc[current_date, 'total'] / portfolio.loc[previous_date, 'total'] - 1
            )
        
        self.portfolio = portfolio
        self.positions = positions
        
        return portfolio
