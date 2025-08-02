from config import (
    USE_FIXED_LOT_SIZE,
    LOT_SIZE,
    RISK_PER_TRADE,
    ATR_SL_MULTIPLIER,
    REWARD_RISK_RATIO,
    TRADE_PERCENTAGE
)

def calculate_lot_size(balance, stop_loss_pips):
    """
    Calculates the trade volume (lot size) based on the chosen method in config.py.
    For OANDA, this returns lot size which will be converted to units later.
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

def calculate_units(balance, stop_loss_pips):
    """
    Calculates the number of units for OANDA based on risk management.
    
    Args:
        balance (float): Account balance
        stop_loss_pips (float): Stop loss in pips
        
    Returns:
        int: Number of units to trade
    """
    if USE_FIXED_LOT_SIZE:
        # Convert lot size to units (1 lot = 100,000 units)
        return int(LOT_SIZE * 100000)
    
    # Calculate lot size first
    lot_size = calculate_lot_size(balance, stop_loss_pips)
    
    # Convert to units (1 lot = 100,000 units for forex)
    units = int(lot_size * 100000)
    
    # Ensure minimum units (1000 units = 0.01 lot)
    return max(1000, units)

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

def calculate_position_size_for_balance(balance, price, stop_loss_pips):
    """
    Calculate position size based on account balance and risk percentage.
    
    Args:
        balance (float): Account balance
        price (float): Current price
        stop_loss_pips (float): Stop loss in pips
        
    Returns:
        int: Number of units to trade
    """
    # Calculate risk amount
    risk_amount = balance * RISK_PER_TRADE
    
    # For forex, 1 pip = $10 per standard lot (100,000 units)
    # So 1 pip = $0.0001 per unit for most major pairs
    pip_value_per_unit = 0.0001
    
    # Calculate units based on risk
    units = int(risk_amount / (stop_loss_pips * pip_value_per_unit))
    
    # Ensure minimum units (1000 units = 0.01 lot)
    return max(1000, units)

def calculate_position_size(balance, stop_loss_pips):
    """
    Legacy function for backward compatibility.
    Calculates position size based on account balance and risk percentage.
    
    Args:
        balance (float): Account balance
        stop_loss_pips (float): Stop loss in pips
        
    Returns:
        float: Lot size for trading
    """
    if USE_FIXED_LOT_SIZE:
        return LOT_SIZE
    
    # Calculate lot size based on risk
    risk_amount = balance * RISK_PER_TRADE
    
    # For forex, 1 pip = $10 per standard lot
    value_per_pip_per_lot = 10.0
    
    # Calculate required lot size to match the risk amount
    calculated_lots = risk_amount / (stop_loss_pips * value_per_pip_per_lot)
    
    # Return the calculated lot size, rounded to 2 decimal places, but not less than 0.01
    return max(0.01, round(calculated_lots, 2)) 