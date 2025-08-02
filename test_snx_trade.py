import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from trader_interface import MultiTrader
from strategy import generate_signal
from risk import calculate_units, get_sl_tp
from config import TIMEFRAME, ATR_SL_MULTIPLIER
from utils import setup_logger

def test_snx_trade():
    """Test placing a trade on SNX/USD BUY signal"""
    logger = setup_logger('snx_test')
    
    print("🚀 Testing SNX/USD BUY Signal Trade...")
    
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
        
        # Test SNX/USD
        symbol = "SNX/USD"
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
        
        if signal != "buy":
            print("⚠️  Expected BUY signal not found")
            return
            
        # Calculate position size (smaller risk for testing)
        risk_amount = 2.0  # $2 risk for testing
        current_price = multi_trader.get_current_price(symbol)
        if not current_price:
            print("❌ Failed to get current price")
            return
            
        entry_price = current_price['ask']  # Use ask price for BUY
        print(f"💰 Entry price: ${entry_price:.4f}")
        
        # Calculate stop loss and take profit
        sl_pips = atr * ATR_SL_MULTIPLIER
        tp_pips = sl_pips * 1.5  # 1.5:1 reward/risk ratio
        
        sl_price = entry_price - sl_pips
        tp_price = entry_price + tp_pips
        
        # Calculate position size based on available balance
        available_balance = balance * 0.05  # Use only 5% of balance for tight trades
        
        # Add a safety buffer for Kraken fees
        available_balance -= 1.0  # Reserve $1 for fees/slippage
        amount = available_balance / entry_price
        
        # Kraken may reject too many decimals (e.g., >8)
        amount = round(amount, 6)
        
        # Ensure minimum order size for Kraken (usually $10-20 minimum)
        min_order_value = 20.0  # $20 minimum
        min_amount = min_order_value / entry_price
        
        if amount < min_amount:
            amount = min_amount
            print(f"⚠️  Adjusted to minimum order size: {amount:.6f} SNX")
        
        # Ensure we don't exceed available balance
        max_order_value = balance * 0.08  # Use 8% of balance max
        max_amount = max_order_value / entry_price
        
        if amount > max_amount:
            amount = max_amount
            print(f"⚠️  Adjusted to maximum order size: {amount:.6f} SNX")
        
        print(f"📊 Position size: {amount:.6f} SNX")
        print(f"🛑 Stop loss pips: {sl_pips:.4f}")
        print(f"🛑 Stop Loss: ${sl_price:.4f}")
        print(f"🎯 Take Profit: ${tp_price:.4f}")
        print(f"⚠️  Risk amount: ${risk_amount:.2f}")
        
        # Ask for confirmation
        print(f"\n🤔 Ready to place BUY order:")
        print(f"   Amount: {amount:.6f} SNX")
        print(f"   Entry: ${entry_price:.4f}")
        print(f"   SL: ${sl_price:.4f}")
        print(f"   TP: ${tp_price:.4f}")
        print(f"   Risk: ${risk_amount:.2f}")
        
        confirm = input("Do you want to place this SNX trade? (y/n): ").lower().strip()
        
        if confirm == 'y':
            # Place the order
            success = multi_trader.place_order(
                symbol=symbol,
                direction="buy",
                units=amount,
                sl=sl_price,
                tp=tp_price
            )
            
            if success:
                print("✅ SNX trade placed successfully!")
                print("📱 Check your Telegram for trade notification")
            else:
                print("❌ Failed to place SNX trade")
        else:
            print("❌ Trade cancelled by user")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        logger.error(f"Error in SNX trade test: {e}")
    finally:
        multi_trader.disconnect_all()

if __name__ == "__main__":
    test_snx_trade() 