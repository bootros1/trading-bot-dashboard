import oandapyV20
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.pricing as pricing
from oandapyV20.exceptions import V20Error
import pandas as pd
from datetime import datetime, timedelta
import time
from typing import List

from config import (
    OANDA_API_KEY, 
    OANDA_ACCOUNT_ID, 
    OANDA_ENVIRONMENT, 
    OANDA_BASE_URL,
    OANDA_SYMBOLS,
    TIMEFRAME
)
from utils import setup_logger
from notifier import send_telegram
from trader_interface import TraderInterface

logger = setup_logger('oanda_broker')

class OandaBroker(TraderInterface):
    """
    OANDA REST API broker implementation.
    Handles authentication, order placement, account info, and price data.
    """
    
    def __init__(self):
        """Initialize OANDA client with API credentials."""
        self.client = None
        self.account_id = OANDA_ACCOUNT_ID
        self.connected = False
    
    def connect(self) -> bool:
        """Connect to OANDA API."""
        try:
            self.client = oandapyV20.API(
                access_token=OANDA_API_KEY,
                environment=OANDA_ENVIRONMENT
            )
            self.connected = True
            logger.info("OANDA client initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize OANDA client: {e}")
            self.connected = False
            return False
    
    def disconnect(self) -> None:
        """Disconnect from OANDA API."""
        self.client = None
        self.connected = False
        logger.info("OANDA connection closed")
    
    def get_account_info(self):
        """
        Get account information including balance and margin.
        Returns: dict with account details or None if failed
        """
        if not self.connected:
            return None
            
        try:
            r = accounts.AccountDetails(accountID=self.account_id)
            response = self.client.request(r)
            
            account_info = {
                'balance': float(response['account']['balance']),
                'currency': response['account']['currency'],
                'margin_used': float(response['account']['marginUsed']),
                'margin_available': float(response['account']['marginAvailable']),
                'open_trade_count': int(response['account']['openTradeCount']),
                'open_position_count': int(response['account']['openPositionCount'])
            }
            
            logger.info(f"Account balance: {account_info['balance']} {account_info['currency']}")
            return account_info
            
        except V20Error as e:
            logger.error(f"OANDA API error getting account info: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting account info: {e}")
            return None
    
    def get_historical_data(self, symbol, timeframe, bars=100):
        """
        Get historical price data for a symbol.
        
        Args:
            symbol (str): Symbol in OANDA format (e.g., 'EUR_USD')
            timeframe (str): Timeframe (e.g., 'M15', 'H1', 'D')
            bars (int): Number of bars to retrieve
            
        Returns:
            pandas.DataFrame: OHLCV data or None if failed
        """
        if not self.connected:
            return None
            
        try:
            # Convert timeframe to OANDA format
            granularity = self._convert_timeframe(timeframe)
            logger.info(f"Requesting {bars} bars of {granularity} data for {symbol}")
            
            # Get candles with count parameter (simpler approach)
            r = instruments.InstrumentsCandles(
                instrument=symbol,
                params={
                    "granularity": granularity,
                    "count": bars
                }
            )
            
            response = self.client.request(r)
            logger.info(f"Received response for {symbol}: {len(response.get('candles', []))} candles")
            
            if 'candles' not in response or not response['candles']:
                logger.warning(f"No historical data received for {symbol}")
                return None
            
            # Convert to DataFrame
            data = []
            for candle in response['candles']:
                if candle['complete']:  # Only use complete candles
                    data.append({
                        'time': pd.to_datetime(candle['time']),
                        'open': float(candle['mid']['o']),
                        'high': float(candle['mid']['h']),
                        'low': float(candle['mid']['l']),
                        'close': float(candle['mid']['c']),
                        'volume': int(candle.get('volume', 0))
                    })
            
            df = pd.DataFrame(data)
            logger.info(f"Retrieved {len(df)} bars for {symbol}")
            return df
            
        except V20Error as e:
            logger.error(f"OANDA API error getting historical data for {symbol}: {e}")
            logger.error(f"Error details: {e.__dict__}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting historical data for {symbol}: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return None
    
    def place_order(self, symbol, direction, units, sl=None, tp=None):
        """
        Place a market order with optional stop-loss and take-profit.
        
        Args:
            symbol (str): Symbol in OANDA format (e.g., 'EUR_USD')
            direction (str): 'buy' or 'sell'
            units (int): Number of units (positive for buy, negative for sell)
            sl (float): Stop-loss price (optional)
            tp (float): Take-profit price (optional)
            
        Returns:
            bool: True if order placed successfully, False otherwise
        """
        if not self.connected:
            return False
            
        try:
            # Prepare order data
            order_data = {
                "order": {
                    "type": "MARKET",
                    "instrument": symbol,
                    "units": str(units) if direction == 'buy' else str(-units),
                    "timeInForce": "FOK",
                    "positionFill": "DEFAULT"
                }
            }
            
            # Add stop-loss if provided
            if sl is not None:
                order_data["order"]["stopLossOnFill"] = {
                    "price": str(sl),
                    "timeInForce": "GTC"
                }
            
            # Add take-profit if provided
            if tp is not None:
                order_data["order"]["takeProfitOnFill"] = {
                    "price": str(tp),
                    "timeInForce": "GTC"
                }
            
            # Place order
            r = orders.OrderCreate(accountID=self.account_id, data=order_data)
            response = self.client.request(r)
            
            if response['orderFillTransaction']:
                fill_transaction = response['orderFillTransaction']
                price = float(fill_transaction['price'])
                units_filled = int(fill_transaction['units'])
                
                logger.info(f"Order placed successfully: {direction} {units_filled} units of {symbol} at {price}")
                send_telegram(
                    f"✅ Trade executed:\nSymbol: {symbol}\nDirection: {direction}\nUnits: {units_filled}\nPrice: {price:.5f}\nSL: {sl:.5f if sl else 'None'}\nTP: {tp:.5f if tp else 'None'}"
                )
                return True
            else:
                logger.error("Order placed but no fill transaction received")
                return False
                
        except V20Error as e:
            logger.error(f"OANDA API error placing order: {e}")
            send_telegram(
                f"❌ Trade FAILED:\nSymbol: {symbol}\nDirection: {direction}\nUnits: {units}\nError: {str(e)}"
            )
            return False
        except Exception as e:
            logger.error(f"Unexpected error placing order: {e}")
            send_telegram(
                f"❌ Trade FAILED:\nSymbol: {symbol}\nDirection: {direction}\nUnits: {units}\nError: {str(e)}"
            )
            return False
    
    def get_current_price(self, symbol):
        """
        Get current bid/ask prices for a symbol.
        
        Args:
            symbol (str): Symbol in OANDA format
            
        Returns:
            dict: {'bid': float, 'ask': float} or None if failed
        """
        if not self.connected:
            return None
            
        try:
            r = pricing.PricingInfo(accountID=self.account_id, params={"instruments": symbol})
            response = self.client.request(r)
            
            if response['prices']:
                price_info = response['prices'][0]
                return {
                    'bid': float(price_info['bids'][0]['price']),
                    'ask': float(price_info['asks'][0]['price'])
                }
            return None
            
        except Exception as e:
            logger.error(f"Error getting current price for {symbol}: {e}")
            return None
    
    def get_open_trades(self):
        """
        Get list of open trades.
        
        Returns:
            list: List of open trades or empty list if failed
        """
        if not self.connected:
            return []
            
        try:
            r = trades.OpenTrades(accountID=self.account_id)
            response = self.client.request(r)
            
            return response.get('trades', [])
            
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
            r = orders.OrderCancel(accountID=self.account_id, orderID=order_id)
            response = self.client.request(r)
            logger.info(f"Order {order_id} cancelled successfully")
            return True
        except Exception as e:
            logger.error(f"Error cancelling order {order_id}: {e}")
            return False
    
    def get_symbols(self) -> List[str]:
        """Get list of available trading symbols."""
        return OANDA_SYMBOLS
    
    def get_timeframes(self) -> List[str]:
        """Get list of available timeframes."""
        return ['M1', 'M5', 'M15', 'M30', 'H1', 'H4', 'D', 'W', 'M']
    
    def _convert_timeframe(self, timeframe):
        """
        Convert timeframe string to OANDA granularity format.
        
        Args:
            timeframe (str): Timeframe like 'M15', 'H1', 'D'
            
        Returns:
            str: OANDA granularity format
        """
        timeframe_map = {
            'M1': 'M1',
            'M5': 'M5', 
            'M15': 'M15',
            'M30': 'M30',
            'H1': 'H1',
            'H4': 'H4',
            'D': 'D',
            'W': 'W',
            'M': 'M'
        }
        
        return timeframe_map.get(timeframe, 'M15')
    
    def _get_minutes_per_bar(self, granularity):
        """
        Get minutes per bar for a given granularity.
        
        Args:
            granularity (str): OANDA granularity format
            
        Returns:
            int: Minutes per bar
        """
        minutes_map = {
            'M1': 1,
            'M5': 5,
            'M15': 15,
            'M30': 30,
            'H1': 60,
            'H4': 240,
            'D': 1440,
            'W': 10080,
            'M': 43200
        }
        
        return minutes_map.get(granularity, 15)

# Global broker instance
oanda_broker = None

def initialize_broker():
    """Initialize the global OANDA broker instance."""
    global oanda_broker
    try:
        oanda_broker = OandaBroker()
        return oanda_broker.connect()
    except Exception as e:
        logger.error(f"Failed to initialize OANDA broker: {e}")
        return False

def get_broker():
    """Get the global broker instance."""
    return oanda_broker

# Legacy function names for compatibility
def connect():
    """Legacy function for compatibility with existing code."""
    return initialize_broker()

def disconnect():
    """Legacy function for compatibility with existing code."""
    if oanda_broker:
        oanda_broker.disconnect()

def get_account_info():
    """Legacy function for compatibility with existing code."""
    broker = get_broker()
    if broker:
        return broker.get_account_info()
    return None

def get_historical_data(symbol, timeframe, bars=100):
    """Legacy function for compatibility with existing code."""
    broker = get_broker()
    if broker:
        return broker.get_historical_data(symbol, timeframe, bars)
    return None

def place_order(symbol, direction, lot, sl, tp):
    """
    Legacy function for compatibility with existing code.
    Converts lot size to units and places order.
    """
    broker = get_broker()
    if not broker:
        return False
    
    # Convert lot size to units (1 lot = 100,000 units for forex)
    units = int(lot * 100000)
    
    return broker.place_order(symbol, direction, units, sl, tp) 