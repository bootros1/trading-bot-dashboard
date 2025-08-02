#!/usr/bin/env python3
"""
Test script to place a small trade and verify order execution.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from oanda_broker import initialize_broker, get_broker
    from utils import setup_logger
    
    logger = setup_logger('test_trade')
    
    def test_order_placement():
        """Test placing a small order to verify functionality."""
        print("🧪 Testing Order Placement...")
        
        # Initialize broker
        if not initialize_broker():
            print("❌ Failed to initialize OANDA broker")
            return False
        
        broker = get_broker()
        if not broker:
            print("❌ No broker instance available")
            return False
        
        # Get account info
        account_info = broker.get_account_info()
        if not account_info:
            print("❌ Failed to get account info")
            return False
        
        print(f"✅ Account Balance: {account_info['balance']} {account_info['currency']}")
        
        # Test symbol
        symbol = "EUR_USD"
        
        # Get current price
        prices = broker.get_current_price(symbol)
        if not prices:
            print(f"❌ Failed to get current price for {symbol}")
            return False
        
        print(f"✅ Current {symbol} price:")
        print(f"   Bid: {prices['bid']:.5f}")
        print(f"   Ask: {prices['ask']:.5f}")
        
        # Calculate test parameters
        direction = 'buy'  # or 'sell'
        test_units = 1000  # Minimum units (0.01 lot)
        
        # Simple SL/TP (10 pips each)
        if direction == 'buy':
            entry_price = prices['ask']
            sl = entry_price - 0.0010  # 10 pips below
            tp = entry_price + 0.0010  # 10 pips above
        else:
            entry_price = prices['bid']
            sl = entry_price + 0.0010  # 10 pips above
            tp = entry_price - 0.0010  # 10 pips below
        
        print(f"\n📊 Test Trade Parameters:")
        print(f"   Symbol: {symbol}")
        print(f"   Direction: {direction}")
        print(f"   Units: {test_units}")
        print(f"   Entry: {entry_price:.5f}")
        print(f"   Stop Loss: {sl:.5f}")
        print(f"   Take Profit: {tp:.5f}")
        
        # Ask for confirmation
        response = input("\n🤔 Do you want to place this test trade? (y/n): ")
        if response.lower() != 'y':
            print("❌ Test trade cancelled")
            return False
        
        # Place the order
        print(f"\n🚀 Placing test order...")
        success = broker.place_order(symbol, direction, test_units, sl, tp)
        
        if success:
            print("✅ Test order placed successfully!")
            print("📱 Check your Telegram for confirmation")
            return True
        else:
            print("❌ Test order failed")
            return False
    
    if __name__ == "__main__":
        test_order_placement()
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc() 