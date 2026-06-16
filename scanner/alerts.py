import logging
from datetime import datetime
from typing import List, Dict

logger = logging.getLogger(__name__)

class AlertManager:
    """Manage alerts and notifications for trading signals."""
    
    def __init__(self):
        self.alerts = []
        self.alert_count = 0
    
    def create_alert(self, analysis: Dict) -> None:
        """Create an alert from analysis results."""
        alert = {
            'id': self.alert_count,
            'timestamp': datetime.now().isoformat(),
            'coin_id': analysis['coin_id'],
            'current_price': analysis['current_price'],
            'signals': analysis['signals'],
            'price_change_24h': analysis['price_change_24h'],
            'momentum': analysis['momentum'],
            'rsi': analysis['rsi'],
            'read': False
        }
        
        self.alerts.append(alert)
        self.alert_count += 1
        
        self._log_alert(alert)
    
    def _log_alert(self, alert: Dict) -> None:
        """Log alert details."""
        logger.warning(
            f"ALERT #{alert['id']}: {alert['coin_id'].upper()} - "
            f"Price: ${alert['current_price']:.2f} - "
            f"Signals: {', '.join(alert['signals'])}"
        )
    
    def get_alerts(self, unread_only: bool = False) -> List[Dict]:
        """Get alerts with optional filtering."""
        if unread_only:
            return [a for a in self.alerts if not a['read']]
        return self.alerts
    
    def mark_as_read(self, alert_id: int) -> bool:
        """Mark an alert as read."""
        for alert in self.alerts:
            if alert['id'] == alert_id:
                alert['read'] = True
                return True
        return False
    
    def clear_alerts(self) -> None:
        """Clear all alerts."""
        self.alerts = []
        logger.info("All alerts cleared")
