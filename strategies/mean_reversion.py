import pandas as pd
import numpy as np

class MeanReversionStrategy:
    def __init__(self, window=20, threshold=2.0):
        self.window = window
        self.threshold = threshold
        self.name = f"MeanReversion_{window}_{threshold}"
        
    def generate_signals(self, data):
        """
        Generate trading signals based on mean reversion (Bollinger Bands)
        """
        signals = pd.DataFrame(index=data.index)
        signals['price'] = data['Close']
        signals['bb_middle'] = data['bb_middle']
        signals['bb_upper'] = data['bb_upper']
        signals['bb_lower'] = data['bb_lower']
        
        # Create signals
        signals['signal'] = 0.0
        signals['signal'] = np.where(
            signals['price'] < signals['bb_lower'], 1.0, 0.0)
        signals['signal'] = np.where(
            signals['price'] > signals['bb_upper'], -1.0, signals['signal'])
        
        # Generate trading orders
        signals['positions'] = signals['signal'].diff()
        
        return signals
