# Quantitative Trading Strategy Simulator

A comprehensive backtesting framework for quantitative trading strategies.

## Features

- Data fetching from Yahoo Finance and Alpha Vantage
- Multiple trading strategies (SMA Crossover, Mean Reversion, Momentum)
- Backtesting engine with performance metrics
- Parameter optimization using grid search
- Command-line interface for easy use
- Visualization of results

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`

## Usage

### Fetch data
python main.py --fetch-data --ticker AAPL --start-date 2020-01-01 --end-date 2023-01-01

### Run backtest with SMA strategy
python main.py --strategy SMA --short-window 20 --long-window 50 --plot


### Optimize strategy parameters
python main.py --strategy SMA --optimize --plot


### Run with different strategy
python main.py --strategy MeanReversion --threshold 2.0 --plot


## Project Structure

- `data/`: Raw and processed financial data
- `strategies/`: Trading strategy implementations
- `backtester/`: Backtesting engine and performance metrics
- `optimizers/`: Parameter optimization tools
- `cli/`: Command-line interface
- `utils/`: Data fetching and processing utilities
- `reports/`: Generated reports
- `visualizations/`: Generated plots and charts

## Supported Strategies

1. **SMA Crossover**: Buy when short-term MA crosses above long-term MA, sell when it crosses below
2. **Mean Reversion**: Buy when price is below lower Bollinger Band, sell when above upper Band
3. **Momentum**: Buy when RSI is oversold, sell when overbought

## Performance Metrics

- Sharpe Ratio
- Sortino Ratio
- Maximum Drawdown
- Annualized Return
- Calmar Ratio


Deployment Instructions

Install dependencies:
bash
pip install -r requirements.txt
Make the CLI executable:
bash
chmod +x main.py
Create necessary directories:
bash
mkdir -p data/raw_data data/processed_data reports visualizations
Run the simulator:
bash
# Fetch data first
python main.py --fetch-data --ticker AAPL --start-date 2020-01-01 --end-date 2023-01-01

# Then run a strategy
python main.py --strategy SMA --short-window 20 --long-window 50 --plot
  
