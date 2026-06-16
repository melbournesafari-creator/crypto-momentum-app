import logging
from typing import List, Dict
from config import RSI_PERIOD, MACD_FAST, MACD_SLOW, MACD_SIGNAL

logger = logging.getLogger(__name__)

class TechnicalIndicators:
    """Calculate technical indicators for cryptocurrency analysis."""
    
    @staticmethod
    def calculate_sma(prices: List[float], period: int) -> float:
        """Calculate Simple Moving Average."""
        if len(prices) < period:
            return None
        return sum(prices[-period:]) / period
    
    @staticmethod
    def calculate_ema(prices: List[float], period: int) -> float:
        """Calculate Exponential Moving Average."""
        if len(prices) < period:
            return None
        
        multiplier = 2 / (period + 1)
        ema = sum(prices[:period]) / period
        
        for price in prices[period:]:
            ema = (price * multiplier) + (ema * (1 - multiplier))
        
        return ema
    
    @staticmethod
    def calculate_rsi(prices: List[float], period: int = RSI_PERIOD) -> float:
        """Calculate Relative Strength Index."""
        if len(prices) < period + 1:
            return None
        
        gains = []
        losses = []
        
        for i in range(1, len(prices)):
            change = prices[i] - prices[i-1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))
        
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        
        if avg_loss == 0:
            return 100 if avg_gain > 0 else 50
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    @staticmethod
    def calculate_macd(prices: List[float], fast: int = MACD_FAST, slow: int = MACD_SLOW, signal: int = MACD_SIGNAL) -> Dict:
        """Calculate MACD (Moving Average Convergence Divergence)."""
        if len(prices) < slow:
            return None
        
        ema_fast = TechnicalIndicators.calculate_ema(prices, fast)
        ema_slow = TechnicalIndicators.calculate_ema(prices, slow)
        
        if ema_fast is None or ema_slow is None:
            return None
        
        macd_line = ema_fast - ema_slow
        
        return {
            'macd_line': macd_line,
            'signal_line': None,  # Would need list of MACD values to calculate
            'histogram': None
        }
    
    @staticmethod
    def calculate_momentum(prices: List[float], period: int = 14) -> float:
        """Calculate price momentum."""
        if len(prices) < period + 1:
            return None
        
        current = prices[-1]
        previous = prices[-period-1]
        
        if previous == 0:
            return 0
        
        momentum = ((current - previous) / previous) * 100
        return momentum
    
    @staticmethod
    def calculate_bollinger_bands(prices: List[float], period: int = 20, std_dev: int = 2) -> Dict:
        """Calculate Bollinger Bands."""
        if len(prices) < period:
            return None
        
        sma = TechnicalIndicators.calculate_sma(prices, period)
        
        # Calculate standard deviation
        variance = sum((x - sma) ** 2 for x in prices[-period:]) / period
        std = variance ** 0.5
        
        return {
            'upper_band': sma + (std * std_dev),
            'middle_band': sma,
            'lower_band': sma - (std * std_dev)
        }
