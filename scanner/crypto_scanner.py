import logging
import time
from datetime import datetime, timedelta
from typing import List, Dict
import requests
from config import (
    SCAN_INTERVAL,
    MAX_COINS,
    MOMENTUM_THRESHOLD,
    VOLUME_SPIKE_MULTIPLIER,
    ALERT_ON_MOMENTUM,
    ALERT_ON_VOLUME_SPIKE,
    ALERT_ON_BREAKOUT,
    API_TIMEOUT,
    REQUEST_RETRIES
)
from .indicators import TechnicalIndicators
from .alerts import AlertManager

logger = logging.getLogger(__name__)

class CryptoScanner:
    """Main cryptocurrency scanner for detecting momentum and trading opportunities."""
    
    def __init__(self):
        self.api_url = "https://api.coingecko.com/api/v3"
        self.technical_indicators = TechnicalIndicators()
        self.alert_manager = AlertManager()
        self.price_history = {}  # Store historical prices for indicators
        self.running = False
        
    def get_top_coins(self, limit: int = MAX_COINS) -> List[str]:
        """Fetch top cryptocurrencies by market cap."""
        try:
            url = f"{self.api_url}/coins/markets"
            params = {
                'order': 'market_cap_desc',
                'per_page': min(limit, 250),
                'page': 1,
                'sparkline': False
            }
            response = requests.get(url, params=params, timeout=API_TIMEOUT)
            response.raise_for_status()
            coins = response.json()
            return [coin['id'] for coin in coins]
        except Exception as e:
            logger.error(f"Error fetching top coins: {e}")
            return []
    
    def get_coin_data(self, coin_id: str, days: int = 7) -> Dict:
        """Fetch cryptocurrency historical data."""
        try:
            url = f"{self.api_url}/coins/{coin_id}/market_chart"
            params = {
                'vs_currency': 'usd',
                'days': days,
                'interval': 'daily'
            }
            response = requests.get(url, params=params, timeout=API_TIMEOUT)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching data for {coin_id}: {e}")
            return None
    
    def analyze_coin(self, coin_id: str) -> Dict:
        """Analyze a single cryptocurrency for trading signals."""
        data = self.get_coin_data(coin_id)
        if not data:
            return None
        
        prices = [p[1] for p in data.get('prices', [])]
        volumes = [v[1] for v in data.get('total_volumes', [])]
        
        if len(prices) < 2:
            return None
        
        # Calculate metrics
        current_price = prices[-1]
        price_change_24h = ((prices[-1] - prices[-2]) / prices[-2]) * 100
        momentum = self.technical_indicators.calculate_momentum(prices)
        rsi = self.technical_indicators.calculate_rsi(prices)
        macd = self.technical_indicators.calculate_macd(prices)
        
        # Volume analysis
        avg_volume = sum(volumes[-7:]) / 7 if len(volumes) >= 7 else sum(volumes) / len(volumes)
        current_volume = volumes[-1]
        volume_spike = (current_volume / avg_volume) if avg_volume > 0 else 0
        
        return {
            'coin_id': coin_id,
            'timestamp': datetime.now().isoformat(),
            'current_price': current_price,
            'price_change_24h': price_change_24h,
            'momentum': momentum,
            'rsi': rsi,
            'macd': macd,
            'volume_spike': volume_spike,
            'signals': self._generate_signals(momentum, rsi, volume_spike, price_change_24h)
        }
    
    def _generate_signals(self, momentum: float, rsi: float, volume_spike: float, price_change: float) -> List[str]:
        """Generate trading signals based on analysis."""
        signals = []
        
        if ALERT_ON_MOMENTUM and abs(momentum) > MOMENTUM_THRESHOLD:
            signals.append(f"MOMENTUM: {momentum:.2f}%")
        
        if ALERT_ON_VOLUME_SPIKE and volume_spike > VOLUME_SPIKE_MULTIPLIER:
            signals.append(f"VOLUME_SPIKE: {volume_spike:.2f}x")
        
        if ALERT_ON_BREAKOUT:
            if rsi > 70:
                signals.append("OVERBOUGHT")
            elif rsi < 30:
                signals.append("OVERSOLD")
        
        return signals
    
    def scan(self) -> List[Dict]:
        """Run a complete scan of cryptocurrencies."""
        logger.info("Starting cryptocurrency scan...")
        coins = self.get_top_coins()
        results = []
        
        for coin_id in coins:
            analysis = self.analyze_coin(coin_id)
            if analysis and analysis.get('signals'):
                results.append(analysis)
                logger.info(f"{coin_id}: {analysis['signals']}")
        
        return results
    
    def start(self):
        """Start continuous scanning."""
        self.running = True
        logger.info("Scanner started")
        
        try:
            while self.running:
                results = self.scan()
                for result in results:
                    self.alert_manager.create_alert(result)
                time.sleep(SCAN_INTERVAL)
        except KeyboardInterrupt:
            logger.info("Scanner stopped by user")
            self.stop()
    
    def stop(self):
        """Stop the scanner."""
        self.running = False
        logger.info("Scanner stopped")
