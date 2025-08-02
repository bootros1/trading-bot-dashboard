import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from trader_interface import MultiTrader
from strategy import generate_signal
from config import TIMEFRAME
from utils import setup_logger

def test_extended_crypto_pairs():
    """Test additional crypto pairs beyond the configured ones"""
    logger = setup_logger('extended_crypto_test')
    
    print("🚀 Testing Extended Crypto Pairs for Trading Signals...")
    
    # Initialize multi-trader with Kraken
    multi_trader = MultiTrader("KRAKEN")
    
    try:
        # Add and connect to Kraken
        if not multi_trader.add_broker("KRAKEN"):
            print("❌ Failed to connect to Kraken")
            return
            
        # Test additional popular crypto pairs
        extended_pairs = [
            'MATIC/USD', 'FTM/USD', 'AVAX/USD', 'ATOM/USD', 'NEAR/USD',
            'ALGO/USD', 'LINK/USD', 'UNI/USD', 'AAVE/USD', 'SUSHI/USD',
            'SNX/USD', 'COMP/USD', 'MKR/USD', 'YFI/USD', 'CRV/USD',
            'BAL/USD', 'REN/USD', 'ZRX/USD', 'BAND/USD', 'KNC/USD',
            'STORJ/USD', 'MANA/USD', 'SAND/USD', 'AXS/USD', 'ENJ/USD',
            'CHZ/USD', 'HOT/USD', 'VET/USD', 'TRX/USD', 'ADA/USD',
            'DOT/USD', 'LINK/USD', 'LTC/USD', 'BCH/USD', 'XLM/USD',
            'XMR/USD', 'ZEC/USD', 'DASH/USD', 'ETC/USD', 'XRP/USD'
        ]
        
        print(f"📊 Testing {len(extended_pairs)} additional crypto pairs...")
        print("=" * 60)
        
        signals_found = []
        no_signals = []
        
        for i, symbol in enumerate(extended_pairs, 1):
            try:
                print(f"🔍 [{i:2d}/{len(extended_pairs)}] Testing {symbol}...", end=" ")
                
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
                    print(f"✅ {signal.upper()} signal - ${price:.4f}")
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
        print("📊 EXTENDED SIGNAL SUMMARY")
        print("=" * 60)
        
        if signals_found:
            print(f"🎯 Found {len(signals_found)} additional trading signals:")
            for signal in signals_found:
                print(f"   {signal['signal'].upper()} {signal['symbol']} @ ${signal['price']:.4f}")
        else:
            print("⚠️  No additional trading signals found")
            
        print(f"\n📈 Pairs with signals: {len(signals_found)}")
        print(f"⏸️  Pairs without signals: {len(no_signals)}")
        print(f"📊 Total pairs tested: {len(extended_pairs)}")
        
        # Show top 10 pairs without signals
        if no_signals:
            print(f"\n⏸️  Top 10 pairs without signals:")
            for i, symbol in enumerate(no_signals[:10], 1):
                print(f"   {i}. {symbol}")
        
        return signals_found
        
    except Exception as e:
        print(f"❌ Error: {e}")
        logger.error(f"Error in extended crypto test: {e}")
        return []
    finally:
        multi_trader.disconnect_all()

def test_high_volume_pairs():
    """Test high-volume pairs that are more likely to have signals"""
    print("\n🎯 Testing High-Volume Crypto Pairs...")
    
    # Initialize multi-trader with Kraken
    multi_trader = MultiTrader("KRAKEN")
    
    try:
        # Add and connect to Kraken
        if not multi_trader.add_broker("KRAKEN"):
            print("❌ Failed to connect to Kraken")
            return
            
        # Test high-volume pairs
        high_volume_pairs = [
            'BTC/USD', 'ETH/USD', 'XRP/USD', 'ADA/USD', 'DOT/USD',
            'LTC/USD', 'BCH/USD', 'LINK/USD', 'UNI/USD', 'SOL/USD',
            'AVAX/USD', 'ATOM/USD', 'NEAR/USD', '1INCH/USD', 'AAVE/USD',
            'ALGO/USD', 'ALICE/USD', 'APT/USD', 'ARB/USD', 'AXS/USD',
            'MATIC/USD', 'FTM/USD', 'SUSHI/USD', 'SNX/USD', 'COMP/USD'
        ]
        
        signals_found = []
        
        for symbol in high_volume_pairs:
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
                    print(f"✅ {signal.upper()} signal - ${price:.4f}")
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
                print(f"   {signal['signal'].upper()} {signal['symbol']} @ ${signal['price']:.4f}")
        
        return signals_found
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return []
    finally:
        multi_trader.disconnect_all()

if __name__ == "__main__":
    print("🚀 Extended Crypto Pair Signal Scanner")
    print("=" * 50)
    
    # Test extended pairs
    extended_signals = test_extended_crypto_pairs()
    
    # Test high-volume pairs
    high_volume_signals = test_high_volume_pairs()
    
    print(f"\n🎉 Extended scan complete!")
    print(f"📊 Total additional signals found: {len(extended_signals) + len(high_volume_signals)}") 