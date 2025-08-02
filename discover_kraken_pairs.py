import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import ccxt
from config import KRAKEN_API_KEY, KRAKEN_API_SECRET

def discover_kraken_pairs():
    """Discover all available USD trading pairs on Kraken"""
    print("🔍 Discovering Kraken USD Trading Pairs...")
    
    try:
        # Initialize Kraken client
        kraken = ccxt.kraken({
            'apiKey': KRAKEN_API_KEY,
            'secret': KRAKEN_API_SECRET,
            'sandbox': False,
            'enableRateLimit': True,
        })
        
        # Load markets
        print("📊 Loading markets...")
        markets = kraken.load_markets()
        
        # Find all USD pairs
        usd_pairs = []
        for symbol in markets:
            if "/USD" in symbol:
                usd_pairs.append(symbol)
        
        # Sort by popularity/volume (common pairs first)
        popular_pairs = [
            'BTC/USD', 'ETH/USD', 'XRP/USD', 'ADA/USD', 'DOT/USD',
            'LTC/USD', 'BCH/USD', 'LINK/USD', 'UNI/USD', 'MATIC/USD',
            'SOL/USD', 'AVAX/USD', 'ATOM/USD', 'FTM/USD', 'NEAR/USD'
        ]
        
        # Sort pairs: popular first, then alphabetically
        sorted_pairs = []
        for pair in popular_pairs:
            if pair in usd_pairs:
                sorted_pairs.append(pair)
                usd_pairs.remove(pair)
        
        # Add remaining pairs alphabetically
        sorted_pairs.extend(sorted(usd_pairs))
        
        print(f"\n✅ Found {len(sorted_pairs)} USD trading pairs:")
        print("=" * 60)
        
        # Display pairs in columns
        for i in range(0, len(sorted_pairs), 3):
            row = sorted_pairs[i:i+3]
            formatted_row = [f"{pair:<15}" for pair in row]
            print("  ".join(formatted_row))
        
        print("=" * 60)
        print(f"📊 Total USD pairs available: {len(sorted_pairs)}")
        
        # Generate config update
        print("\n📝 Config update for config.py:")
        print("KRAKEN_SYMBOLS = [")
        for pair in sorted_pairs[:20]:  # Top 20 pairs
            print(f"    '{pair}',")
        print("]")
        
        return sorted_pairs
        
    except Exception as e:
        print(f"❌ Error discovering pairs: {e}")
        return []

def test_pair_availability():
    """Test which pairs have good liquidity and are actively traded"""
    print("\n🧪 Testing pair availability and liquidity...")
    
    try:
        kraken = ccxt.kraken({
            'apiKey': KRAKEN_API_KEY,
            'secret': KRAKEN_API_SECRET,
            'sandbox': False,
            'enableRateLimit': True,
        })
        
        # Test pairs for ticker data
        test_pairs = [
            'BTC/USD', 'ETH/USD', 'XRP/USD', 'ADA/USD', 'DOT/USD',
            'LTC/USD', 'BCH/USD', 'LINK/USD', 'UNI/USD', 'MATIC/USD',
            'SOL/USD', 'AVAX/USD', 'ATOM/USD', 'FTM/USD', 'NEAR/USD'
        ]
        
        available_pairs = []
        
        for pair in test_pairs:
            try:
                ticker = kraken.fetch_ticker(pair)
                if ticker and ticker['last']:
                    print(f"✅ {pair}: ${ticker['last']:.2f}")
                    available_pairs.append(pair)
                else:
                    print(f"❌ {pair}: No data")
            except Exception as e:
                print(f"❌ {pair}: {e}")
        
        print(f"\n🎯 Recommended trading pairs: {len(available_pairs)} available")
        return available_pairs
        
    except Exception as e:
        print(f"❌ Error testing pairs: {e}")
        return []

if __name__ == "__main__":
    print("🚀 Kraken Pair Discovery Tool")
    print("=" * 40)
    
    # Discover all pairs
    all_pairs = discover_kraken_pairs()
    
    # Test availability
    available_pairs = test_pair_availability()
    
    print(f"\n🎉 Discovery complete!")
    print(f"📊 Total USD pairs: {len(all_pairs)}")
    print(f"✅ Available for trading: {len(available_pairs)}") 