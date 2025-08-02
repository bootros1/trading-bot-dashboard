import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from trader_interface import MultiTrader
from config import get_symbols
from utils import setup_logger

def test_simple_order():
    """Test placing a simple market order on Kraken"""
    logger = setup_logger('simple_order_test')
    
    print("🚀 Testing Simple Kraken Order...")
    
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
        
        # Test with a small amount
        symbol = "1INCH/USD"
        amount = 10.0  # Small amount for testing
        
        print(f"📈 Testing simple order: {amount} 1INCH")
        
        # Place simple market order without SL/TP
        success = multi_trader.place_order(
            symbol=symbol,
            direction="buy",
            units=amount,
            sl=None,
            tp=None
        )
        
        if success:
            print("✅ Simple order placed successfully!")
        else:
            print("❌ Failed to place simple order")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        logger.error(f"Error in simple order test: {e}")
    finally:
        multi_trader.disconnect_all()

if __name__ == "__main__":
    test_simple_order() 