#!/usr/bin/env python3
"""
OANDA Connection Test Script
Tests the OANDA API connection and basic functionality.
"""

import sys
import os
from datetime import datetime

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from oanda_broker import initialize_broker, get_broker
    from config import SYMBOLS, TIMEFRAME
    from utils import setup_logger
    
    logger = setup_logger('test_oanda')
    
    def test_connection():
        """Test OANDA API connection."""
        print("🔌 Testing OANDA API connection...")
        
        if initialize_broker():
            print("✅ OANDA client initialized successfully")
            return True
        else:
            print("❌ Failed to initialize OANDA client")
            return False
    
    def test_account_info():
        """Test account information retrieval."""
        print("\n📊 Testing account information...")
        
        broker = get_broker()
        if not broker:
            print("❌ No broker instance available")
            return False
        
        account_info = broker.get_account_info()
        if account_info:
            print(f"✅ Account info retrieved successfully")
            print(f"   Balance: {account_info['balance']} {account_info['currency']}")
            print(f"   Margin Used: {account_info['margin_used']}")
            print(f"   Margin Available: {account_info['margin_available']}")
            print(f"   Open Trades: {account_info['open_trade_count']}")
            print(f"   Open Positions: {account_info['open_position_count']}")
            return True
        else:
            print("❌ Failed to get account information")
            return False
    
    def test_historical_data():
        """Test historical data retrieval."""
        print(f"\n📈 Testing historical data retrieval...")
        
        broker = get_broker()
        if not broker:
            print("❌ No broker instance available")
            return False
        
        success_count = 0
        for symbol in SYMBOLS[:3]:  # Test first 3 symbols
            print(f"   Testing {symbol}...")
            df = broker.get_historical_data(symbol, TIMEFRAME, bars=10)
            if df is not None and not df.empty:
                print(f"   ✅ {symbol}: {len(df)} bars retrieved")
                print(f"      Latest price: {df.iloc[-1]['close']:.5f}")
                success_count += 1
            else:
                print(f"   ❌ {symbol}: Failed to retrieve data")
        
        print(f"\n📊 Historical data test: {success_count}/{len(SYMBOLS[:3])} symbols successful")
        return success_count > 0
    
    def test_current_prices():
        """Test current price retrieval."""
        print(f"\n💰 Testing current price retrieval...")
        
        broker = get_broker()
        if not broker:
            print("❌ No broker instance available")
            return False
        
        success_count = 0
        for symbol in SYMBOLS[:3]:  # Test first 3 symbols
            print(f"   Testing {symbol}...")
            prices = broker.get_current_price(symbol)
            if prices:
                print(f"   ✅ {symbol}: Bid {prices['bid']:.5f}, Ask {prices['ask']:.5f}")
                success_count += 1
            else:
                print(f"   ❌ {symbol}: Failed to get current price")
        
        print(f"\n💰 Current price test: {success_count}/{len(SYMBOLS[:3])} symbols successful")
        return success_count > 0
    
    def test_open_trades():
        """Test open trades retrieval."""
        print(f"\n📋 Testing open trades retrieval...")
        
        broker = get_broker()
        if not broker:
            print("❌ No broker instance available")
            return False
        
        trades = broker.get_open_trades()
        if trades is not None:
            print(f"✅ Open trades retrieved: {len(trades)} trades")
            for trade in trades:
                print(f"   Trade ID: {trade['id']}, Instrument: {trade['instrument']}")
            return True
        else:
            print("❌ Failed to retrieve open trades")
            return False
    
    def run_all_tests():
        """Run all tests."""
        print("🚀 Starting OANDA API Tests")
        print("=" * 50)
        
        tests = [
            ("Connection", test_connection),
            ("Account Info", test_account_info),
            ("Historical Data", test_historical_data),
            ("Current Prices", test_current_prices),
            ("Open Trades", test_open_trades)
        ]
        
        results = []
        for test_name, test_func in tests:
            try:
                result = test_func()
                results.append((test_name, result))
            except Exception as e:
                print(f"❌ {test_name} test failed with exception: {e}")
                results.append((test_name, False))
        
        # Summary
        print("\n" + "=" * 50)
        print("📋 TEST SUMMARY")
        print("=" * 50)
        
        passed = 0
        for test_name, result in results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{test_name:20} {status}")
            if result:
                passed += 1
        
        print(f"\nOverall: {passed}/{len(results)} tests passed")
        
        if passed == len(results):
            print("🎉 All tests passed! Your OANDA setup is working correctly.")
        else:
            print("⚠️  Some tests failed. Please check your configuration.")
        
        return passed == len(results)
    
    if __name__ == "__main__":
        success = run_all_tests()
        sys.exit(0 if success else 1)

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install required packages: pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1) 