import pandas as pd
import numpy as np

class SMAStrategy:
    def __init__(self, short_window=20, long_window=50):
        self.short_window = short_window
        self.long_window = long_window
        self.name = f"SMA_{short_window}_{long_window}"
        
    def generate_signals(self, data):
        """
        Generate trading signals based on SMA crossover
        """
        signals = pd.DataFrame(index=data.index)
        signals['price'] = data['Close']
        signals['short_mavg'] = data['sma_short']
        signals['long_mavg'] = data['sma_long']
        
        # Create signals
        signals['signal'] = 0.0
        signals['signal'][self.short_window:] = np.where(
            signals['short_mavg'][self.short_window:] > signals['long_mavg'][self.short_window:], 1.0, 0.0)
        
        # Generate trading orders
        signals['positions'] = signals['signal'].diff()
        
        return signals
