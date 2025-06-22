from config import (
    USE_FIXED_LOT_SIZE,
    LOT_SIZE,
    RISK_PER_TRADE,
    ATR_SL_MULTIPLIER,
    REWARD_RISK_RATIO
)

def calculate_lot_size(balance, stop_loss_pips):
    """
    Calculates the trade volume (lot size) based on the chosen method in config.py.
    """
    if USE_FIXED_LOT_SIZE:
        return LOT_SIZE

    # --- Dynamic Lot Size Calculation ---
    if stop_loss_pips <= 0:
        # Avoid division by zero and invalid trades
        return 0.01  # Default to minimum lot size as a fallback

    # Risk amount in account currency (e.g., USD)
    risk_amount = balance * RISK_PER_TRADE

    # This is a simplification. For a multi-currency portfolio, this needs to be
    # dynamic based on the quote currency of the pair.
    # For major USD-quoted pairs (EURUSD, GBPUSD), this is ~$10 per standard lot.
    value_per_pip_per_lot = 10.0

    # Calculate required lot size to match the risk amount
    calculated_lots = risk_amount / (stop_loss_pips * value_per_pip_per_lot)

    # Return the calculated lot size, rounded to 2 decimal places, but not less than 0.01
    return max(0.01, round(calculated_lots, 2))


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