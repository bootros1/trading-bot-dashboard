from config import RISK_PER_TRADE, TRADE_PERCENTAGE, ATR_SL_MULTIPLIER, REWARD_RISK_RATIO

def calculate_position_size(balance, stop_loss_pips):
    """Calculates position size based on account balance and stop-loss in pips."""
    # Risk per trade in account currency
    risk_amount = balance * RISK_PER_TRADE
    
    # Value per pip (for a standard lot of a 5-digit broker, e.g., EURUSD)
    # This might need to be adjusted or made dynamic based on the symbol
    pip_value_per_lot = 10
    
    if stop_loss_pips <= 0:
        return 0.01 # Return minimum lot size if SL is zero to avoid division by zero

    # Calculate lot size
    lots = risk_amount / (stop_loss_pips * pip_value_per_lot)

    # Ensure it doesn't exceed the max allowed trade percentage (a secondary check)
    # This part of the logic may need refinement based on margin requirements
    # For now, we'll keep the primary calculation based on risk per trade.
    
    return max(round(lots, 2), 0.01) # Return at least the minimum lot size


def get_sl_tp(price, direction, atr):
    """Calculates Stop-Loss and Take-Profit levels based on ATR."""
    if atr is None or atr == 0:
        return None, None

    sl_distance = atr * ATR_SL_MULTIPLIER
    tp_distance = sl_distance * REWARD_RISK_RATIO

    if direction == 'buy':
        sl = price - sl_distance
        tp = price + tp_distance
    else:  # 'sell'
        sl = price + sl_distance
        tp = price - tp_distance
        
    return sl, tp 