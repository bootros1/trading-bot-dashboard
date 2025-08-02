"""
Kraken API Client for Crypto Trading
Implements the TraderInterface for Kraken exchange.
"""

import ccxt
import pandas as pd
from datetime import datetime, timedelta
import time
from typing import Dict, List, Optional, Any

from config import (
    KRAKEN_API_KEY,
    KRAKEN_API_SECRET,
    KRAKEN_SYMBOLS,
    TIMEFRAME
)
from utils import setup_logger
from notifier import send_telegram
from trader_interface import TraderInterface

logger = setup_logger('kraken_client')

class KrakenClient(TraderInterface):
    """
    Kraken exchange client implementation.
    Handles authentication, order placement, account info, and price data.
    """
    
    def __init__(self):
        """Initialize Kraken client with API credentials."""
        self.exchange = None
        self.connected = False
        self.api_key = KRAKEN_API_KEY
        self.api_secret = KRAKEN_API_SECRET
        
        # Default symbols for crypto trading
        self.default_symbols = [
            'BTC/USD', 'ETH/USD', 'XRP/USD', 'ADA/USD', 'DOT/USD',
            'BTC/EUR', 'ETH/EUR', 'XRP/EUR', 'ADA/EUR', 'DOT/EUR'
        ]
    
    def connect(self) -> bool:
        """Connect to Kraken API."""
        try:
            self.exchange = ccxt.kraken({
                'apiKey': self.api_key,
                'secret': self.api_secret,
                'sandbox': False,  # Kraken doesn't support sandbox in CCXT
                'enableRateLimit': True,
            })
            
            # Test connection by fetching balance
            self.exchange.load_markets()
            self.connected = True
            logger.info("Kraken client initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Kraken client: {e}")
            self.connected = False
            return False
    
    def disconnect(self) -> None:
        """Disconnect from Kraken API."""
        self.exchange = None
        self.connected = False
        logger.info("Kraken connection closed")
    
    def get_account_info(self) -> Optional[Dict[str, Any]]:
        """
        Get account information including balance.
        
        Returns:
            dict: Account information or None if failed
        """
        if not self.connected:
            return None
            
        try:
            balance = self.exchange.fetch_balance()
            
            # Calculate total balance in USD
            total_balance = 0.0
            for currency, amount in balance['total'].items():
                if amount > 0:
                    try:
                        # Get ticker for USD conversion
                        if currency != 'USD':
                            ticker = self.exchange.fetch_ticker(f"{currency}/USD")
                            total_balance += amount * ticker['last']
                        else:
                            total_balance += amount
                    except:
                        # If conversion fails, just add the amount
                        total_balance += amount
            
            account_info = {
                'balance': total_balance,
                'currency': 'USD',
                'margin_used': 0.0,  # Kraken doesn't provide this directly
                'margin_available': total_balance,
                'open_trade_count': len(balance.get('info', {}).get('open_orders', [])),
                'open_position_count': len(balance.get('info', {}).get('open_positions', []))
            }
            
            logger.info(f"Account balance: {account_info['balance']} USD")
            return account_info
            
        except Exception as e:
            logger.error(f"Error getting account info: {e}")
            return None
    
    def get_historical_data(self, symbol: str, timeframe: str, bars: int = 100) -> Optional[pd.DataFrame]:
        """
        Get historical price data for a symbol.
        
        Args:
            symbol (str): Symbol in Kraken format (e.g., 'BTC/USD')
            timeframe (str): Timeframe (e.g., '15m', '1h', '1d')
            bars (int): Number of bars to retrieve
            
        Returns:
            pandas.DataFrame: OHLCV data or None if failed
        """
        if not self.connected:
            return None
            
        try:
            # Convert timeframe to CCXT format
            ccxt_timeframe = self._convert_timeframe(timeframe)
            
            # Fetch OHLCV data
            ohlcv = self.exchange.fetch_ohlcv(symbol, ccxt_timeframe, limit=bars)
            
            if not ohlcv:
                logger.warning(f"No historical data received for {symbol}")
                return None
            
            # Convert to DataFrame
            df = pd.DataFrame(ohlcv, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
            df['time'] = pd.to_datetime(df['time'], unit='ms')
            
            logger.info(f"Retrieved {len(df)} bars for {symbol}")
            return df
            
        except Exception as e:
            logger.error(f"Error getting historical data for {symbol}: {e}")
            return None
    
    def get_current_price(self, symbol: str) -> Optional[Dict[str, float]]:
        """
        Get current bid/ask prices for a symbol.
        
        Args:
            symbol (str): Symbol in Kraken format
            
        Returns:
            dict: {'bid': float, 'ask': float} or None if failed
        """
        if not self.connected:
            return None
            
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return {
                'bid': float(ticker['bid']),
                'ask': float(ticker['ask'])
            }
        except Exception as e:
            logger.error(f"Error getting current price for {symbol}: {e}")
            return None
    
    def place_order(self, symbol: str, direction: str, units: float, sl: Optional[float] = None, tp: Optional[float] = None) -> bool:
        """
        Place a market order with optional stop-loss and take-profit.
        
        Args:
            symbol (str): Symbol in Kraken format (e.g., 'BTC/USD')
            direction (str): 'buy' or 'sell'
            units (float): Amount to trade
            sl (float): Stop-loss price (optional)
            tp (float): Take-profit price (optional)
            
        Returns:
            bool: True if order placed successfully, False otherwise
        """
        if not self.connected:
            return False
            
        try:
            # Place market order
            order_type = 'market'
            side = direction.lower()
            
            order_params = {}
            
            # Add stop-loss if provided
            if sl is not None:
                if side == 'buy':
                    order_params['stopLoss'] = {'price': str(sl)}
                else:
                    order_params['stopLoss'] = {'price': str(sl)}
            
            # Add take-profit if provided
            if tp is not None:
                if side == 'buy':
                    order_params['takeProfit'] = {'price': str(tp)}
                else:
                    order_params['takeProfit'] = {'price': str(tp)}
            
            # Place the order
            order = self.exchange.create_order(
                symbol=symbol,
                type=order_type,
                side=side,
                amount=units,
                params=order_params
            )
            
            if order and order.get('id'):
                logger.info(f"Order placed successfully: {direction} {units} of {symbol}")
                send_telegram(
                    f"✅ Trade executed:\nSymbol: {symbol}\nDirection: {direction}\nAmount: {units}\nOrder ID: {order['id']}\nSL: {sl if sl else 'None'}\nTP: {tp if tp else 'None'}"
                )
                return True
            else:
                logger.error("Order placed but no order ID received")
                return False
                
        except Exception as e:
            logger.error(f"Error placing order: {e}")
            send_telegram(
                f"❌ Trade FAILED:\nSymbol: {symbol}\nDirection: {direction}\nAmount: {units}\nError: {str(e)}"
            )
            return False
    
    def get_open_trades(self) -> List[Dict[str, Any]]:
        """
        Get list of open trades.
        
        Returns:
            list: List of open trades or empty list if failed
        """
        if not self.connected:
            return []
            
        try:
            open_orders = self.exchange.fetch_open_orders()
            return open_orders
        except Exception as e:
            logger.error(f"Error getting open trades: {e}")
            return []
    
    def cancel_order(self, order_id: str) -> bool:
        """
        Cancel an open order.
        
        Args:
            order_id (str): Order ID to cancel
            
        Returns:
            bool: True if order cancelled successfully
        """
        if not self.connected:
            return False
            
        try:
            result = self.exchange.cancel_order(order_id)
            logger.info(f"Order {order_id} cancelled successfully")
            return True
        except Exception as e:
            logger.error(f"Error cancelling order {order_id}: {e}")
            return False
    
    def get_symbols(self) -> List[str]:
        """Get list of available trading symbols."""
        if not self.connected:
            return self.default_symbols
            
        try:
            markets = self.exchange.load_markets()
            return list(markets.keys())
        except Exception as e:
            logger.error(f"Error getting symbols: {e}")
            return self.default_symbols
    
    def get_timeframes(self) -> List[str]:
        """Get list of available timeframes."""
        return ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w', '1M']
    
    def _convert_timeframe(self, timeframe: str) -> str:
        """
        Convert timeframe string to CCXT format.
        
        Args:
            timeframe (str): Timeframe like 'M15', 'H1', 'D'
            
        Returns:
            str: CCXT timeframe format
        """
        timeframe_map = {
            'M1': '1m',
            'M5': '5m', 
            'M15': '15m',
            'M30': '30m',
            'H1': '1h',
            'H4': '4h',
            'D': '1d',
            'W': '1w',
            'M': '1M'
        }
        
        return timeframe_map.get(timeframe, '15m')

# Global client instance
kraken_client = None

def initialize_client():
    """Initialize the global Kraken client instance."""
    global kraken_client
    try:
        kraken_client = KrakenClient()
        return kraken_client.connect()
    except Exception as e:
        logger.error(f"Failed to initialize Kraken client: {e}")
        return False

def get_client():
    """Get the global client instance."""
    return kraken_client

# Legacy function names for compatibility
def connect():
    """Legacy function for compatibility with existing code."""
    return initialize_client()

def disconnect():
    """Legacy function for compatibility with existing code."""
    if kraken_client:
        kraken_client.disconnect()

def get_account_info():
    """Legacy function for compatibility with existing code."""
    client = get_client()
    if client:
        return client.get_account_info()
    return None

def get_historical_data(symbol, timeframe, bars=100):
    """Legacy function for compatibility with existing code."""
    client = get_client()
    if client:
        return client.get_historical_data(symbol, timeframe, bars)
    return None

def place_order(symbol, direction, lot, sl, tp):
    """
    Legacy function for compatibility with existing code.
    Converts lot size to amount and places order.
    """
    client = get_client()
    if not client:
        return False
    
    # For crypto, use the amount directly (no lot size conversion needed)
    amount = lot
    
    return client.place_order(symbol, direction, amount, sl, tp) 