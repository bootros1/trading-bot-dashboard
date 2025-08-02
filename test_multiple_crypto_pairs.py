import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from trader_interface import MultiTrader
from strategy import generate_signal
from config import get_symbols, TIMEFRAME
from utils import setup_logger

def test_multiple_crypto_pairs():
    """Test multiple crypto pairs to find trading signals"""
    logger = setup_logger('multi_crypto_test')
    
    print("🚀 Testing Multiple Crypto Pairs for Trading Signals...")
    
    # Initialize multi-trader with Kraken
    multi_trader = MultiTrader("KRAKEN")
    
    try:
        # Add and connect to Kraken
        if not multi_trader.add_broker("KRAKEN"):
            print("❌ Failed to connect to Kraken")
            return
            
        # Get symbols
        symbols = get_symbols()
        if not symbols:
            print("❌ No trading symbols available")
            return
            
        print(f"📊 Testing {len(symbols)} crypto pairs...")
        print("=" * 60)
        
        signals_found = []
        no_signals = []
        
        for i, symbol in enumerate(symbols, 1):
            try:
                print(f"🔍 [{i:2d}/{len(symbols)}] Testing {symbol}...", end=" ")
                
                # Get historical data
                data = multi_trader.get_historical_data(symbol, TIMEFRAME, 100)
                if data is None or len(data) < 20:
                    print("❌ Insufficient data")
                    no_signals.append(symbol)
                    continue
                
                # Get current price
                current_price = multi_trader.get_current_price(symbol)
                if not current_price:
                    print("❌ No price data")
                    no_signals.append(symbol)
                    continue
                
                # Generate signal
                signal, atr = generate_signal(data)
                
                if signal:
                    price = current_price['bid']
                    print(f"✅ {signal.upper()} signal - ${price:.2f}")
                    signals_found.append({
                        'symbol': symbol,
                        'signal': signal,
                        'price': price,
                        'atr': atr
                    })
                else:
                    print("⏸️  No signal")
                    no_signals.append(symbol)
                    
            except Exception as e:
                print(f"❌ Error: {e}")
                no_signals.append(symbol)
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 SIGNAL SUMMARY")
        print("=" * 60)
        
        if signals_found:
            print(f"🎯 Found {len(signals_found)} trading signals:")
            for signal in signals_found:
                print(f"   {signal['signal'].upper()} {signal['symbol']} @ ${signal['price']:.2f}")
        else:
            print("⚠️  No trading signals found")
            
        print(f"\n📈 Pairs with signals: {len(signals_found)}")
        print(f"⏸️  Pairs without signals: {len(no_signals)}")
        print(f"📊 Total pairs tested: {len(symbols)}")
        
        # Show top 5 pairs without signals
        if no_signals:
            print(f"\n⏸️  Top 5 pairs without signals:")
            for i, symbol in enumerate(no_signals[:5], 1):
                print(f"   {i}. {symbol}")
        
        return signals_found
        
    except Exception as e:
        print(f"❌ Error: {e}")
        logger.error(f"Error in multi-crypto test: {e}")
        return []
    finally:
        multi_trader.disconnect_all()

def test_specific_pairs():
    """Test specific pairs that are likely to have signals"""
    print("\n🎯 Testing Specific High-Volume Pairs...")
    
    # Initialize multi-trader with Kraken
    multi_trader = MultiTrader("KRAKEN")
    
    try:
        # Add and connect to Kraken
        if not multi_trader.add_broker("KRAKEN"):
            print("❌ Failed to connect to Kraken")
            return
            
        # Test specific pairs
        test_pairs = [
            'BTC/USD', 'ETH/USD', 'XRP/USD', 'ADA/USD', 'DOT/USD',
            'LTC/USD', 'BCH/USD', 'LINK/USD', 'UNI/USD', 'SOL/USD'
        ]
        
        signals_found = []
        
        for symbol in test_pairs:
            try:
                print(f"🔍 Testing {symbol}...", end=" ")
                
                # Get historical data
                data = multi_trader.get_historical_data(symbol, TIMEFRAME, 100)
                if data is None or len(data) < 20:
                    print("❌ Insufficient data")
                    continue
                
                # Get current price
                current_price = multi_trader.get_current_price(symbol)
                if not current_price:
                    print("❌ No price data")
                    continue
                
                # Generate signal
                signal, atr = generate_signal(data)
                
                if signal:
                    price = current_price['bid']
                    print(f"✅ {signal.upper()} signal - ${price:.2f}")
                    signals_found.append({
                        'symbol': symbol,
                        'signal': signal,
                        'price': price,
                        'atr': atr
                    })
                else:
                    print("⏸️  No signal")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
        
        if signals_found:
            print(f"\n🎯 Found {len(signals_found)} signals in high-volume pairs:")
            for signal in signals_found:
                print(f"   {signal['signal'].upper()} {signal['symbol']} @ ${signal['price']:.2f}")
        
        return signals_found
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return []
    finally:
        multi_trader.disconnect_all()

if __name__ == "__main__":
    print("🚀 Multi-Crypto Pair Signal Scanner")
    print("=" * 50)
    
    # Test all configured pairs
    all_signals = test_multiple_crypto_pairs()
    
    # Test specific high-volume pairs
    specific_signals = test_specific_pairs()
    
    print(f"\n🎉 Scan complete!")
    print(f"📊 Total signals found: {len(all_signals) + len(specific_signals)}") 