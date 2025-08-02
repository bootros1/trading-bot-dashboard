"""
Unified Trader Interface
Abstracts trading functionality across different brokers/exchanges.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Any
import pandas as pd

class TraderInterface(ABC):
    """
    Abstract base class for trading operations.
    All broker implementations must inherit from this class.
    """
    
    @abstractmethod
    def connect(self) -> bool:
        """Connect to the trading platform."""
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect from the trading platform."""
        pass
    
    @abstractmethod
    def get_account_info(self) -> Optional[Dict[str, Any]]:
        """Get account information including balance."""
        pass
    
    @abstractmethod
    def get_historical_data(self, symbol: str, timeframe: str, bars: int = 100) -> Optional[pd.DataFrame]:
        """Get historical price data for a symbol."""
        pass
    
    @abstractmethod
    def get_current_price(self, symbol: str) -> Optional[Dict[str, float]]:
        """Get current bid/ask prices for a symbol."""
        pass
    
    @abstractmethod
    def place_order(self, symbol: str, direction: str, units: float, sl: Optional[float] = None, tp: Optional[float] = None) -> bool:
        """Place a market order with optional stop-loss and take-profit."""
        pass
    
    @abstractmethod
    def get_open_trades(self) -> List[Dict[str, Any]]:
        """Get list of open trades."""
        pass
    
    @abstractmethod
    def cancel_order(self, order_id: str) -> bool:
        """Cancel an open order."""
        pass
    
    @abstractmethod
    def get_symbols(self) -> List[str]:
        """Get list of available trading symbols."""
        pass
    
    @abstractmethod
    def get_timeframes(self) -> List[str]:
        """Get list of available timeframes."""
        pass

class TraderFactory:
    """
    Factory class to create trader instances based on configuration.
    """
    
    @staticmethod
    def create_trader(broker_type: str) -> TraderInterface:
        """
        Create a trader instance based on the broker type.
        
        Args:
            broker_type (str): "OANDA" or "KRAKEN"
            
        Returns:
            TraderInterface: Trader instance
        """
        if broker_type.upper() == "OANDA":
            from oanda_broker import OandaBroker
            return OandaBroker()
        elif broker_type.upper() == "KRAKEN":
            from kraken_client import KrakenClient
            return KrakenClient()
        else:
            raise ValueError(f"Unsupported broker type: {broker_type}")

class MultiTrader:
    """
    Multi-broker trader that can manage multiple trading platforms.
    """
    
    def __init__(self, primary_broker: str = "OANDA"):
        """
        Initialize multi-trader with primary broker.
        
        Args:
            primary_broker (str): Primary broker ("OANDA" or "KRAKEN")
        """
        self.primary_broker = primary_broker
        self.traders = {}
        self.active_trader = None
    
    def add_broker(self, broker_type: str) -> bool:
        """
        Add a broker to the multi-trader.
        
        Args:
            broker_type (str): "OANDA" or "KRAKEN"
            
        Returns:
            bool: True if broker added successfully
        """
        try:
            trader = TraderFactory.create_trader(broker_type)
            if trader.connect():
                self.traders[broker_type.upper()] = trader
                if not self.active_trader:
                    self.active_trader = trader
                return True
            return False
        except Exception as e:
            print(f"Failed to add broker {broker_type}: {e}")
            return False
    
    def switch_broker(self, broker_type: str) -> bool:
        """
        Switch to a different broker.
        
        Args:
            broker_type (str): "OANDA" or "KRAKEN"
            
        Returns:
            bool: True if switch successful
        """
        if broker_type.upper() in self.traders:
            self.active_trader = self.traders[broker_type.upper()]
            return True
        return False
    
    def get_active_trader(self) -> Optional[TraderInterface]:
        """Get the currently active trader."""
        return self.active_trader
    
    def get_account_info(self) -> Optional[Dict[str, Any]]:
        """Get account info from active trader."""
        if self.active_trader:
            return self.active_trader.get_account_info()
        return None
    
    def get_historical_data(self, symbol: str, timeframe: str, bars: int = 100) -> Optional[pd.DataFrame]:
        """Get historical data from active trader."""
        if self.active_trader:
            return self.active_trader.get_historical_data(symbol, timeframe, bars)
        return None
    
    def place_order(self, symbol: str, direction: str, units: float, sl: Optional[float] = None, tp: Optional[float] = None) -> bool:
        """Place order with active trader."""
        if self.active_trader:
            return self.active_trader.place_order(symbol, direction, units, sl, tp)
        return False
    
    def get_current_price(self, symbol: str) -> Optional[Dict[str, float]]:
        """Get current price from active trader."""
        if self.active_trader:
            return self.active_trader.get_current_price(symbol)
        return None
    
    def get_open_trades(self) -> List[Dict[str, Any]]:
        """Get open trades from active trader."""
        if self.active_trader:
            return self.active_trader.get_open_trades()
        return []
    
    def disconnect_all(self):
        """Disconnect all traders."""
        for trader in self.traders.values():
            try:
                trader.disconnect()
            except:
                pass
        self.traders.clear()
        self.active_trader = None 