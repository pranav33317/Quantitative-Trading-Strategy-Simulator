import pandas as pd
import numpy as np

class MomentumStrategy:
    def __init__(self, window=14, overbought=70, oversold=30):
        self.window = window
        self.overbought = overbought
        self.oversold = oversold
        self.name = f"Momentum_{window}_{overbought}_{oversold}"
        
    def generate_signals(self, data):
        """
        Generate trading signals based on RSI momentum
        """
        signals = pd.DataFrame(index=data.index)
        signals['price'] = data['Close']
        signals['rsi'] = data['rsi']
        
        # Create signals
        signals['signal'] = 0.0
        signals['signal'] = np.where(
            signals['rsi'] < self.oversold, 1.0, 0.0)
        signals['signal'] = np.where(
            signals['rsi'] > self.overbought, -1.0, signals['signal'])
        
        # Generate trading orders
        signals['positions'] = signals['signal'].diff()
        
        return signals
