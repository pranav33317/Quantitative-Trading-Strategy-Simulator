import pandas as pd
import numpy as np

def calculate_sharpe_ratio(returns, risk_free_rate=0.01):
    """
    Calculate Sharpe ratio
    """
    excess_returns = returns - risk_free_rate/252
    sharpe_ratio = np.sqrt(252) * (excess_returns.mean() / (returns.std() + 1e-8))
    return sharpe_ratio

def calculate_max_drawdown(portfolio_value):
    """
    Calculate maximum drawdown
    """
    rolling_max = portfolio_value.cummax()
    drawdown = (portfolio_value - rolling_max) / rolling_max
    max_drawdown = drawdown.min()
    return max_drawdown

def calculate_annualized_return(returns):
    """
    Calculate annualized return
    """
    cumulative_return = (1 + returns).prod() - 1
    annualized_return = (1 + cumulative_return) ** (252 / len(returns)) - 1
    return annualized_return

def calculate_sortino_ratio(returns, risk_free_rate=0.01):
    """
    Calculate Sortino ratio
    """
    excess_returns = returns - risk_free_rate/252
    negative_returns = excess_returns[excess_returns < 0]
    downside_std = negative_returns.std()
    sortino_ratio = np.sqrt(252) * (excess_returns.mean() / (downside_std + 1e-8))
    return sortino_ratio

def calculate_calmar_ratio(annualized_return, max_drawdown):
    """
    Calculate Calmar ratio
    """
    calmar_ratio = annualized_return / abs(max_drawdown) if max_drawdown != 0 else 0
    return calmar_ratio

def calculate_performance_metrics(portfolio):
    """
    Calculate all performance metrics
    """
    returns = portfolio['returns'].dropna()
    portfolio_value = portfolio['total']
    
    metrics = {}
    metrics['sharpe_ratio'] = calculate_sharpe_ratio(returns)
    metrics['max_drawdown'] = calculate_max_drawdown(portfolio_value)
    metrics['annualized_return'] = calculate_annualized_return(returns)
    metrics['sortino_ratio'] = calculate_sortino_ratio(returns)
    metrics['calmar_ratio'] = calculate_calmar_ratio(
        metrics['annualized_return'], metrics['max_drawdown'])
    metrics['total_return'] = (portfolio_value.iloc[-1] / portfolio_value.iloc[0]) - 1
    
    return metrics
