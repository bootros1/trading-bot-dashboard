#!/usr/bin/env python3
"""
Test script to place a small live trade on OANDA.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from trader_interface import MultiTrader
    from strategy import generate_signal
    from risk import calculate_units, get_sl_tp
    from config import BROKER, TIMEFRAME, ATR_SL_MULTIPLIER, get_symbols
    from utils import setup_logger
    
    logger = setup_logger('live_trade_test')
    
    def test_live_trade():
        """Test placing a small live trade on OANDA."""
        print("🚀 Testing Live Trade on OANDA...")
        
        # Create multi-trader with OANDA
        multi_trader = MultiTrader(primary_broker="OANDA")
        
        # Add OANDA broker
        if not multi_trader.add_broker("OANDA"):
            print("❌ Failed to connect to OANDA")
            return False
        
        print("✅ OANDA connected successfully")
        
        # Get account info
        account_info = multi_trader.get_account_info()
        if not account_info:
            print("❌ Failed to get account info")
            return False
        
        balance = account_info['balance']
        print(f"💰 Account Balance: {balance} {account_info['currency']}")
        
        # Test with EUR_USD
        symbol = "EUR_USD"
        print(f"\n📈 Testing {symbol}...")
        
        # Get historical data
        df = multi_trader.get_historical_data(symbol, TIMEFRAME, bars=100)
        if df is None or df.empty:
            print(f"❌ Failed to get historical data for {symbol}")
            return False
        
        print(f"✅ Got {len(df)} bars of historical data")
        
        # Generate signal
        signal, atr = generate_signal(df)
        if not signal or not atr:
            print(f"ℹ️  No signal for {symbol} at this time")
            return False
        
        print(f"🎯 Signal generated: {signal.upper()}, ATR: {atr:.5f}")
        
        # Calculate position size
        pip_size = 0.0001
        sl_pips = (atr * ATR_SL_MULTIPLIER) / pip_size
        units = calculate_units(balance, sl_pips)
        
        print(f"📊 Position size: {units} units")
        print(f"🛑 Stop loss pips: {sl_pips:.2f}")
        
        # Calculate SL/TP
        price = df.iloc[-1]['close']
        sl, tp = get_sl_tp(price, signal, atr)
        
        if not sl or not tp:
            print("❌ Failed to calculate SL/TP")
            return False
        
        print(f"💰 Entry price: {price:.5f}")
        print(f"🛑 Stop Loss: {sl:.5f}")
        print(f"🎯 Take Profit: {tp:.5f}")
        
        # Calculate risk
        risk_amount = balance * 0.01  # 1% risk
        print(f"⚠️  Risk amount: ${risk_amount:.2f}")
        
        # Ask for confirmation
        print(f"\n🤔 Ready to place {signal.upper()} order:")
        print(f"   Symbol: {symbol}")
        print(f"   Units: {units}")
        print(f"   Entry: {price:.5f}")
        print(f"   SL: {sl:.5f}")
        print(f"   TP: {tp:.5f}")
        print(f"   Risk: ${risk_amount:.2f}")
        
        response = input("\nDo you want to place this trade? (y/n): ")
        if response.lower() != 'y':
            print("❌ Trade cancelled")
            return False
        
        # Place the order
        print(f"\n🚀 Placing live order...")
        success = multi_trader.place_order(symbol, signal, units, sl, tp)
        
        if success:
            print("✅ Live trade placed successfully!")
            print("📱 Check your Telegram for confirmation")
            return True
        else:
            print("❌ Live trade failed")
            return False
    
    if __name__ == "__main__":
        success = test_live_trade()
        if success:
            print("\n🎉 Live trade test completed successfully!")
        else:
            print("\n❌ Live trade test failed!")
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