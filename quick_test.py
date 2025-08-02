#!/usr/bin/env python3
"""
Quick OANDA Connection Test
Tests the connection with your actual API key.
"""

import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from oanda_broker import initialize_broker, get_broker
    from config import OANDA_API_KEY, OANDA_ACCOUNT_ID
    
    print("🔌 Testing OANDA Connection...")
    print(f"API Key: {OANDA_API_KEY[:20]}...{OANDA_API_KEY[-10:]}")
    print(f"Account ID: {OANDA_ACCOUNT_ID}")
    print("-" * 50)
    
    # Test connection
    if initialize_broker():
        print("✅ OANDA client initialized successfully")
        
        broker = get_broker()
        if broker:
            # Test account info
            account_info = broker.get_account_info()
            if account_info:
                print(f"✅ Account info retrieved!")
                print(f"   Balance: {account_info['balance']} {account_info['currency']}")
                print(f"   Margin Available: {account_info['margin_available']}")
                print(f"   Open Trades: {account_info['open_trade_count']}")
                
                # Test current price
                prices = broker.get_current_price('EUR_USD')
                if prices:
                    print(f"✅ Current EUR/USD price:")
                    print(f"   Bid: {prices['bid']:.5f}")
                    print(f"   Ask: {prices['ask']:.5f}")
                else:
                    print("❌ Failed to get current price")
            else:
                print("❌ Failed to get account info")
        else:
            print("❌ No broker instance available")
    else:
        print("❌ Failed to initialize OANDA client")
        print("\nPossible issues:")
        print("1. Check your API key is correct")
        print("2. Verify your Account ID")
        print("3. Ensure you're using the demo environment")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install required packages: pip install -r requirements.txt")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc() 