#!/usr/bin/env python3
"""
Simple test script to verify Kraken API credentials.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import ccxt
    from config import KRAKEN_API_KEY, KRAKEN_API_SECRET
    
    def test_kraken_credentials():
        """Test Kraken API credentials."""
        print("🧪 Testing Kraken API Credentials...")
        
        # Check if credentials are set
        if KRAKEN_API_KEY == 'your_kraken_api_key_here':
            print("❌ Please update KRAKEN_API_KEY in config.py")
            return False
        
        if KRAKEN_API_SECRET == 'your_kraken_api_secret_here':
            print("❌ Please update KRAKEN_API_SECRET in config.py")
            return False
        
        print(f"✅ API Key: {KRAKEN_API_KEY[:10]}...")
        print(f"✅ API Secret: {KRAKEN_API_SECRET[:10]}...")
        
        try:
            # Initialize Kraken exchange
            exchange = ccxt.kraken({
                'apiKey': KRAKEN_API_KEY,
                'secret': KRAKEN_API_SECRET,
                'sandbox': False,  # Kraken doesn't support sandbox in CCXT
                'enableRateLimit': True,
            })
            
            print("🔌 Connecting to Kraken...")
            
            # Test connection by loading markets
            exchange.load_markets()
            print("✅ Successfully connected to Kraken!")
            
            # Test fetching balance
            print("📊 Fetching account balance...")
            balance = exchange.fetch_balance()
            
            if balance:
                print("✅ Successfully fetched balance!")
                print(f"   Total balance entries: {len(balance['total'])}")
                
                # Show some balance info
                for currency, amount in balance['total'].items():
                    if amount > 0:
                        print(f"   {currency}: {amount}")
            else:
                print("❌ Failed to fetch balance")
                return False
            
            # Test fetching ticker
            print("📈 Testing price data...")
            ticker = exchange.fetch_ticker('BTC/USD')
            if ticker:
                print(f"✅ BTC/USD Price: ${ticker['last']:.2f}")
            else:
                print("❌ Failed to fetch price data")
                return False
            
            print("🎉 Kraken API credentials are working correctly!")
            return True
            
        except Exception as e:
            print(f"❌ Error connecting to Kraken: {e}")
            return False
    
    if __name__ == "__main__":
        success = test_kraken_credentials()
        sys.exit(0 if success else 1)

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install required packages: pip install ccxt")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1) 