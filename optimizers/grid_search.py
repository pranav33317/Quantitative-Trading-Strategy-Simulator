import itertools
import pandas as pd
from tqdm import tqdm

def grid_search_optimization(data, strategy_class, param_grid):
    """
    Perform grid search optimization for strategy parameters
    """
    results = []
    param_combinations = list(itertools.product(*param_grid.values()))
    
    for params in tqdm(param_combinations, desc="Running grid search"):
        param_dict = dict(zip(param_grid.keys(), params))
        
        # Initialize strategy with current parameters
        strategy = strategy_class(**param_dict)
        
        # Generate signals
        signals = strategy.generate_signals(data)
        
        # Run backtest
        backtester = Backtester()
        portfolio = backtester.run_backtest(data, signals)
        
        # Calculate performance metrics
        metrics = calculate_performance_metrics(portfolio)
        
        # Store results
        result = {
            'parameters': param_dict,
            'metrics': metrics,
            'portfolio': portfolio
        }
        results.append(result)
    
    # Convert results to DataFrame
    results_df = pd.DataFrame([{
        **r['parameters'],
        **r['metrics']
    } for r in results])
    
    return results_df, results
