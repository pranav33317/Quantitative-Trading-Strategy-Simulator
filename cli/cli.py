import argparse
import pandas as pd
from utils.fetch_data import fetch_yahoo_data, save_data, load_data
from utils.data_processor import prepare_data
from strategies.sma_strategy import SMAStrategy
from strategies.mean_reversion import MeanReversionStrategy
from strategies.momentum import MomentumStrategy
from backtester.backtest import Backtester
from backtester.performance import calculate_performance_metrics
from optimizers.grid_search import grid_search_optimization
import matplotlib.pyplot as plt
import os

def main():
    parser = argparse.ArgumentParser(description='Quantitative Trading Strategy Simulator')
    
    # Data commands
    parser.add_argument('--fetch-data', action='store_true', help='Fetch data from Yahoo Finance')
    parser.add_argument('--ticker', type=str, default='AAPL', help='Ticker symbol')
    parser.add_argument('--start-date', type=str, default='2020-01-01', help='Start date for data')
    parser.add_argument('--end-date', type=str, default='2023-01-01', help='End date for data')
    
    # Strategy commands
    parser.add_argument('--strategy', type=str, default='SMA', choices=['SMA', 'MeanReversion', 'Momentum'], help='Trading strategy')
    parser.add_argument('--short-window', type=int, default=20, help='Short window for SMA strategy')
    parser.add_argument('--long-window', type=int, default=50, help='Long window for SMA strategy')
    parser.add_argument('--threshold', type=float, default=2.0, help='Threshold for Mean Reversion strategy')
    parser.add_argument('--overbought', type=int, default=70, help='Overbought level for Momentum strategy')
    parser.add_argument('--oversold', type=int, default=30, help='Oversold level for Momentum strategy')
    
    # Optimization commands
    parser.add_argument('--optimize', action='store_true', help='Run parameter optimization')
    parser.add_argument('--param-grid', type=str, help='Parameter grid for optimization')
    
    # Output commands
    parser.add_argument('--output-dir', type=str, default='results', help='Output directory for results')
    parser.add_argument('--plot', action='store_true', help='Generate plots')
    
    args = parser.parse_args()
    
    # Create output directories
    os.makedirs('data/raw_data', exist_ok=True)
    os.makedirs('data/processed_data', exist_ok=True)
    os.makedirs('reports', exist_ok=True)
    os.makedirs('visualizations', exist_ok=True)
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Fetch data if requested
    if args.fetch_data:
        print(f"Fetching data for {args.ticker} from {args.start_date} to {args.end_date}")
        data = fetch_yahoo_data(args.ticker, args.start_date, args.end_date)
        if data is not None:
            save_data(data, f"{args.ticker}.csv", 'data/raw_data')
        else:
            print("Failed to fetch data")
            return
    
    # Load data
    data = load_data(f"{args.ticker}.csv", 'data/raw_data')
    if data is None:
        print("No data found. Use --fetch-data to download data first.")
        return
    
    # Prepare data
    data = prepare_data(data)
    save_data(data, f"{args.ticker}_processed.csv", 'data/processed_data')
    
    # Select strategy
    if args.strategy == 'SMA':
        strategy = SMAStrategy(short_window=args.short_window, long_window=args.long_window)
    elif args.strategy == 'MeanReversion':
        strategy = MeanReversionStrategy(threshold=args.threshold)
    elif args.strategy == 'Momentum':
        strategy = MomentumStrategy(overbought=args.overbought, oversold=args.oversold)
    
    # Generate signals
    signals = strategy.generate_signals(data)
    
    # Run optimization if requested
    if args.optimize:
        if args.strategy == 'SMA':
            param_grid = {
                'short_window': [10, 20, 30],
                'long_window': [50, 100, 200]
            }
        elif args.strategy == 'MeanReversion':
            param_grid = {
                'window': [10, 20, 30],
                'threshold': [1.5, 2.0, 2.5]
            }
        elif args.strategy == 'Momentum':
            param_grid = {
                'window': [10, 14, 20],
                'overbought': [70, 80],
                'oversold': [20, 30]
            }
        
        print(f"Running optimization for {args.strategy} strategy")
        results_df, results = grid_search_optimization(data, type(strategy), param_grid)
        
        # Save optimization results
        results_df.to_csv(f"{args.output_dir}/optimization_results_{args.strategy}.csv")
        
        # Find best parameters
        best_idx = results_df['sharpe_ratio'].idxmax()
        best_params = results_df.iloc[best_idx].to_dict()
        
        print(f"Best parameters: {best_params}")
        
        # Run backtest with best parameters
        if args.strategy == 'SMA':
            strategy = SMAStrategy(
                short_window=int(best_params['short_window']),
                long_window=int(best_params['long_window'])
            )
        elif args.strategy == 'MeanReversion':
            strategy = MeanReversionStrategy(
                window=int(best_params['window']),
                threshold=best_params['threshold']
            )
        elif args.strategy == 'Momentum':
            strategy = MomentumStrategy(
                window=int(best_params['window']),
                overbought=int(best_params['overbought']),
                oversold=int(best_params['oversold'])
            )
        
        signals = strategy.generate_signals(data)
    
    # Run backtest
    backtester = Backtester()
    portfolio = backtester.run_backtest(data, signals)
    
    # Calculate performance metrics
    metrics = calculate_performance_metrics(portfolio)
    
    # Save results
    portfolio.to_csv(f"{args.output_dir}/portfolio_{args.strategy}.csv")
    with open(f"{args.output_dir}/metrics_{args.strategy}.txt", 'w') as f:
        for key, value in metrics.items():
            f.write(f"{key}: {value}\n")
    
    # Print results
    print("Performance Metrics:")
    for key, value in metrics.items():
        print(f"{key}: {value:.4f}")
    
    # Generate plots if requested
    if args.plot:
        plt.figure(figsize=(12, 8))
        
        # Plot portfolio value
        plt.subplot(2, 1, 1)
        plt.plot(portfolio.index, portfolio['total'], label='Portfolio Value')
        plt.title('Portfolio Value Over Time')
        plt.xlabel('Date')
        plt.ylabel('Value ($)')
        plt.legend()
        plt.grid(True)
        
        # Plot returns
        plt.subplot(2, 1, 2)
        plt.plot(portfolio.index, portfolio['returns'], label='Daily Returns')
        plt.title('Daily Returns')
        plt.xlabel('Date')
        plt.ylabel('Return')
        plt.legend()
        plt.grid(True)
        
        plt.tight_layout()
        plt.savefig(f"{args.output_dir}/portfolio_plot_{args.strategy}.png")
        plt.close()
        
        print(f"Plots saved to {args.output_dir}/portfolio_plot_{args.strategy}.png")

if __name__ == "__main__":
    main()
