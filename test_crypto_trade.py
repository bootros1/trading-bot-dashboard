import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from trader_interface import MultiTrader
from strategy import generate_signal
from risk import calculate_units, get_sl_tp
from config import BROKER, TIMEFRAME, ATR_SL_MULTIPLIER, get_symbols
from utils import setup_logger

def test_crypto_trade():
    """Test placing a small crypto trade on Kraken"""
    logger = setup_logger('crypto_test')
    
    print("🚀 Testing Crypto Trade on Kraken...")
    
    # Initialize multi-trader with Kraken
    multi_trader = MultiTrader("KRAKEN")
    
    try:
        # Add and connect to Kraken
        if not multi_trader.add_broker("KRAKEN"):
            print("❌ Failed to connect to Kraken")
            return
            
        # Get account info
        info = multi_trader.get_account_info()
        if not info:
            print("❌ Failed to get account info")
            return
            
        balance = info.get('balance', 0)
        print(f"✅ Kraken connected successfully")
        print(f"💰 Account Balance: {balance} USD")
        
        # Get symbols
        symbols = get_symbols()
        if not symbols:
            print("❌ No trading symbols available")
            return
            
        # Test with BTC/USD
        symbol = "BTC/USD"
        print(f"📈 Testing {symbol}...")
        
        # Get historical data
        data = multi_trader.get_historical_data(symbol, TIMEFRAME, 100)
        if data is None or len(data) < 20:
            print("❌ Insufficient historical data")
            return
            
        print(f"✅ Got {len(data)} bars of historical data")
        
        # Generate signal
        signal, atr = generate_signal(data)
        print(f"🎯 Signal generated: {signal}")
        
        if signal is None:
            print("⚠️  No trading signal generated")
            return
            
        # Calculate position size (1% risk)
        risk_amount = balance * 0.01  # 1% risk
        current_price = multi_trader.get_current_price(symbol)
        if not current_price:
            print("❌ Failed to get current price")
            return
            
        entry_price = current_price['ask'] if signal == "BUY" else current_price['bid']
        
        # Calculate ATR for stop loss
        atr = data['high'].rolling(14).max() - data['low'].rolling(14).min()
        atr = atr.iloc[-1]
        
        # Calculate stop loss and take profit
        sl_pips = atr * ATR_SL_MULTIPLIER
        tp_pips = sl_pips * 1.5  # 1.5:1 reward/risk ratio
        
        if signal == "BUY":
            sl_price = entry_price - sl_pips
            tp_price = entry_price + tp_pips
        else:
            sl_price = entry_price + sl_pips
            tp_price = entry_price - tp_pips
            
        # Calculate position size in USD
        risk_per_unit = abs(entry_price - sl_price)
        units = risk_amount / risk_per_unit
        
        # Convert to amount for Kraken (amount in base currency)
        amount = units / entry_price
        
        print(f"📊 Position size: {amount:.6f} BTC")
        print(f"🛑 Stop loss pips: {sl_pips:.2f}")
        print(f"💰 Entry price: {entry_price:.2f}")
        print(f"🛑 Stop Loss: {sl_price:.2f}")
        print(f"🎯 Take Profit: {tp_price:.2f}")
        print(f"⚠️  Risk amount: ${risk_amount:.2f}")
        
        # Ask for confirmation
        print(f"\n🤔 Ready to place {signal} order:")
        print(f"   Amount: {amount:.6f} BTC")
        print(f"   Entry: {entry_price:.2f}")
        print(f"   SL: {sl_price:.2f}")
        print(f"   TP: {tp_price:.2f}")
        print(f"   Risk: ${risk_amount:.2f}")
        
        confirm = input("Do you want to place this crypto trade? (y/n): ").lower().strip()
        
        if confirm == 'y':
            # Place the order
            success = multi_trader.place_order(
                symbol=symbol,
                direction=signal.lower(),
                units=amount,
                sl=sl_price,
                tp=tp_price
            )
            
            if success:
                print("✅ Crypto trade placed successfully!")
                print("📱 Check your Telegram for trade notification")
            else:
                print("❌ Failed to place crypto trade")
        else:
            print("❌ Trade cancelled by user")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        logger.error(f"Error in crypto trade test: {e}")
    finally:
        multi_trader.disconnect_all()

if __name__ == "__main__":
    test_crypto_trade() 