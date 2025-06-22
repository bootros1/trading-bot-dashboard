import pandas as pd
from strategy import generate_signal
from risk import calculate_position_size, get_sl_tp
from utils import setup_logger
from config import INITIAL_BALANCE, ATR_SL_MULTIPLIER

logger = setup_logger('backtest')

def run_backtest(df, initial_balance=None):
    if initial_balance is None:
        initial_balance = INITIAL_BALANCE
    balance = initial_balance
    positions = []
    pip_size = 0.0001 # For 5-digit brokers

    for i in range(51, len(df) - 1): # Stop one bar early to prevent index error
        # The window for calculating indicators ends at index i-1
        window = df.iloc[i-51:i].copy()
        signal, atr = generate_signal(window)
        
        if signal and atr:
            # Entry price is the close of the signal bar (i-1)
            entry_price = window.iloc[-1]['close']
            entry_time = window.iloc[-1]['time'] # Get the time of the trade
            
            sl, tp = get_sl_tp(entry_price, signal, atr)
            
            if sl is None or tp is None:
                continue

            sl_pips = abs(entry_price - sl) / pip_size
            tp_pips = abs(entry_price - tp) / pip_size

            lot = calculate_position_size(balance, sl_pips)
            if lot <= 0:
                continue

            # Simulate trade outcome on the bar *after* the signal (bar i)
            trade_bar = df.iloc[i]
            pnl_pips = 0
            
            if signal == 'buy':
                # Check for stop loss first
                if trade_bar['low'] <= sl:
                    pnl_pips = -sl_pips
                # Then check for take profit
                elif trade_bar['high'] >= tp:
                    pnl_pips = tp_pips
                # Otherwise, close at the end of the bar
                else:
                    pnl_pips = (trade_bar['close'] - entry_price) / pip_size
            
            elif signal == 'sell':
                # Check for stop loss first
                if trade_bar['high'] >= sl:
                    pnl_pips = -sl_pips
                # Then check for take profit
                elif trade_bar['low'] <= tp:
                    pnl_pips = tp_pips
                # Otherwise, close at the end of the bar
                else:
                    pnl_pips = (entry_price - trade_bar['close']) / pip_size
            
            # PnL in account currency
            pip_value_per_lot = 10 
            pnl_amount = pnl_pips * lot * pip_value_per_lot
            balance += pnl_amount
            positions.append({'time': entry_time, 'signal': signal, 'price': entry_price, 'lot': lot, 'pnl': pnl_amount, 'balance': balance})
            
    logger.info(f"Backtest complete. Final balance: {balance:.2f}")
    if not positions:
        return pd.DataFrame()
    return pd.DataFrame(positions) 