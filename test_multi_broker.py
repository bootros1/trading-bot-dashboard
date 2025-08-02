#!/usr/bin/env python3
"""
Multi-Broker Test Script
Tests both OANDA and Kraken functionality.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from trader_interface import MultiTrader, TraderFactory
    from config import BROKER, get_symbols
    from utils import setup_logger
    
    logger = setup_logger('multi_broker_test')
    
    def test_broker_connection(broker_type: str):
        """Test connection to a specific broker."""
        print(f"\n🔌 Testing {broker_type} Connection...")
        
        try:
            trader = TraderFactory.create_trader(broker_type)
            if trader.connect():
                print(f"✅ {broker_type} connected successfully")
                
                # Test account info
                account_info = trader.get_account_info()
                if account_info:
                    print(f"   Balance: {account_info['balance']} {account_info['currency']}")
                    print(f"   Margin Available: {account_info['margin_available']}")
                    print(f"   Open Trades: {account_info['open_trade_count']}")
                else:
                    print(f"   ❌ Failed to get account info")
                
                # Test symbols
                symbols = trader.get_symbols()
                print(f"   Available symbols: {len(symbols)}")
                print(f"   Sample symbols: {symbols[:3]}")
                
                # Test current price for first symbol
                if symbols:
                    prices = trader.get_current_price(symbols[0])
                    if prices:
                        print(f"   Current {symbols[0]} price: Bid {prices['bid']:.5f}, Ask {prices['ask']:.5f}")
                    else:
                        print(f"   ❌ Failed to get current price for {symbols[0]}")
                
                trader.disconnect()
                return True
            else:
                print(f"❌ Failed to connect to {broker_type}")
                return False
                
        except Exception as e:
            print(f"❌ Error testing {broker_type}: {e}")
            return False
    
    def test_multi_trader():
        """Test the multi-trader functionality."""
        print("\n🚀 Testing Multi-Trader...")
        
        multi_trader = MultiTrader(primary_broker="OANDA")
        
        # Test adding OANDA
        print("Adding OANDA...")
        if multi_trader.add_broker("OANDA"):
            print("✅ OANDA added successfully")
        else:
            print("❌ Failed to add OANDA")
        
        # Test adding Kraken
        print("Adding Kraken...")
        if multi_trader.add_broker("KRAKEN"):
            print("✅ Kraken added successfully")
        else:
            print("❌ Failed to add Kraken")
        
        # Test switching brokers
        print("\nTesting broker switching...")
        
        # Switch to OANDA
        if multi_trader.switch_broker("OANDA"):
            print("✅ Switched to OANDA")
            account_info = multi_trader.get_account_info()
            if account_info:
                print(f"   OANDA Balance: {account_info['balance']} {account_info['currency']}")
        else:
            print("❌ Failed to switch to OANDA")
        
        # Switch to Kraken
        if multi_trader.switch_broker("KRAKEN"):
            print("✅ Switched to Kraken")
            account_info = multi_trader.get_account_info()
            if account_info:
                print(f"   Kraken Balance: {account_info['balance']} {account_info['currency']}")
        else:
            print("❌ Failed to switch to Kraken")
        
        multi_trader.disconnect_all()
        print("✅ Multi-trader test completed")
    
    def test_current_broker():
        """Test the currently configured broker."""
        print(f"\n🎯 Testing Current Broker: {BROKER}")
        
        multi_trader = MultiTrader(primary_broker=BROKER)
        
        if multi_trader.add_broker(BROKER):
            print(f"✅ {BROKER} connected successfully")
            
            # Test account info
            account_info = multi_trader.get_account_info()
            if account_info:
                print(f"   Balance: {account_info['balance']} {account_info['currency']}")
            
            # Test symbols
            symbols = get_symbols()
            print(f"   Trading symbols: {symbols}")
            
            # Test historical data for first symbol
            if symbols:
                df = multi_trader.get_historical_data(symbols[0], 'M15', bars=10)
                if df is not None:
                    print(f"   Historical data: {len(df)} bars for {symbols[0]}")
                    print(f"   Latest price: {df.iloc[-1]['close']:.5f}")
                else:
                    print(f"   ❌ Failed to get historical data for {symbols[0]}")
            
            multi_trader.disconnect_all()
            return True
        else:
            print(f"❌ Failed to connect to {BROKER}")
            return False
    
    def run_all_tests():
        """Run all tests."""
        print("🧪 Multi-Broker Trading Bot Tests")
        print("=" * 50)
        
        # Test individual brokers
        oanda_success = test_broker_connection("OANDA")
        kraken_success = test_broker_connection("KRAKEN")
        
        # Test multi-trader
        test_multi_trader()
        
        # Test current broker
        current_success = test_current_broker()
        
        # Summary
        print("\n" + "=" * 50)
        print("📋 TEST SUMMARY")
        print("=" * 50)
        print(f"OANDA Connection: {'✅ PASS' if oanda_success else '❌ FAIL'}")
        print(f"Kraken Connection: {'✅ PASS' if kraken_success else '❌ FAIL'}")
        print(f"Current Broker ({BROKER}): {'✅ PASS' if current_success else '❌ FAIL'}")
        
        if oanda_success and kraken_success and current_success:
            print("\n🎉 All tests passed! Multi-broker setup is working correctly.")
        else:
            print("\n⚠️  Some tests failed. Please check your configuration.")
        
        return oanda_success and kraken_success and current_success
    
    if __name__ == "__main__":
        success = run_all_tests()
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