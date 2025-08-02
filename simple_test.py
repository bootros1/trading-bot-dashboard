#!/usr/bin/env python3
"""
Simple test script to verify OANDA functionality.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from trader_interface import MultiTrader
    from config import BROKER, TIMEFRAME, ATR_SL_MULTIPLIER, get_symbols
    from utils import setup_logger
    
    logger = setup_logger('simple_test')
    
    def test_oanda():
        """Test OANDA functionality."""
        print("🧪 Testing OANDA Connection...")
        
        # Create multi-trader with OANDA
        multi_trader = MultiTrader(primary_broker="OANDA")
        
        # Add OANDA broker
        if not multi_trader.add_broker("OANDA"):
            print("❌ Failed to connect to OANDA")
            return False
        
        print("✅ OANDA connected successfully")
        
        # Get account info
        account_info = multi_trader.get_account_info()
        if account_info:
            print(f"   Balance: {account_info['balance']} {account_info['currency']}")
            print(f"   Margin Available: {account_info['margin_available']}")
            print(f"   Open Trades: {account_info['open_trade_count']}")
        else:
            print("   ❌ Failed to get account info")
            return False
        
        # Get symbols
        symbols = get_symbols()
        print(f"   Trading symbols: {symbols}")
        
        # Test historical data for first symbol
        if symbols:
            df = multi_trader.get_historical_data(symbols[0], TIMEFRAME, bars=10)
            if df is not None:
                print(f"   Historical data: {len(df)} bars for {symbols[0]}")
                print(f"   Latest price: {df.iloc[-1]['close']:.5f}")
            else:
                print(f"   ❌ Failed to get historical data for {symbols[0]}")
                return False
        
        # Test current price
        if symbols:
            prices = multi_trader.get_current_price(symbols[0])
            if prices:
                print(f"   Current {symbols[0]} price: Bid {prices['bid']:.5f}, Ask {prices['ask']:.5f}")
            else:
                print(f"   ❌ Failed to get current price for {symbols[0]}")
                return False
        
        multi_trader.disconnect_all()
        print("✅ OANDA test completed successfully")
        return True
        
    if __name__ == "__main__":
        success = test_oanda()
        if success:
            print("\n🎉 OANDA is working correctly!")
        else:
            print("\n❌ OANDA test failed!")
        sys.exit(0 if success else 1)

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install required packages: pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1) 