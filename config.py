# Configuration file for Crypto Scanner

# API Settings
API_TIMEOUT = 10
REQUEST_RETRIES = 3

# Scanner Settings
SCAN_INTERVAL = 60  # seconds
MAX_COINS = 250  # top coins by market cap

# Momentum Detection
MOMENTUM_THRESHOLD = 5.0  # percentage change
VOLUME_SPIKE_MULTIPLIER = 2.0  # volume increase multiplier

# Technical Indicators
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

# Alert Settings
ALERT_ON_MOMENTUM = True
ALERT_ON_VOLUME_SPIKE = True
ALERT_ON_BREAKOUT = True

# Cryptocurrencies to monitor (add more as needed)
CRYPTO_PAIRS = [
    'bitcoin',
    'ethereum',
    'cardano',
    'solana',
    'ripple',
    'polkadot',
    'dogecoin',
    'shiba-inu'
]
