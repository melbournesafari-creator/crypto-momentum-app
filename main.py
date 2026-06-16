#!/usr/bin/env python3
"""
Main entry point for the Crypto Momentum Scanner.
"""

import logging
import sys
from scanner import CryptoScanner

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scanner.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Run the crypto scanner."""
    logger.info("Starting Crypto Momentum Scanner")
    
    try:
        scanner = CryptoScanner()
        scanner.start()
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
