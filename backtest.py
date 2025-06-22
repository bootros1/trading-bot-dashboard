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
            pnl_amount = 0
            exit_price = 0

            # --- BUY ---
            if signal == 'buy':
                # First, check if the low of the bar hits the stop loss
                if trade_bar['low'] <= sl:
                    exit_price = sl
                # Next, check if the high hits the take profit
                elif trade_bar['high'] >= tp:
                    exit_price = tp
                # Otherwise, the trade is closed at the end of the bar
                else:
                    exit_price = trade_bar['close']
                
                pnl_pips = (exit_price - entry_price) / pip_size
                pnl_amount = pnl_pips * lot * 10  # Assuming pip_value_per_lot is 10

            # --- SELL ---
            elif signal == 'sell':
                # First, check if the high of the bar hits the stop loss
                if trade_bar['high'] >= sl:
                    exit_price = sl
                # Next, check if the low hits the take profit
                elif trade_bar['low'] <= tp:
                    exit_price = tp
                # Otherwise, the trade is closed at the end of the bar
                else:
                    exit_price = trade_bar['close']
                
                pnl_pips = (entry_price - exit_price) / pip_size
                pnl_amount = pnl_pips * lot * 10  # Assuming pip_value_per_lot is 10
            
            # Add logging to debug PnL for each trade
            logger.info(f"TRADE: {signal.upper()} | Entry: {entry_price:.5f}, Exit: {exit_price:.5f}, PnL: ${pnl_amount:.2f}")

            # PnL in account currency
            balance += pnl_amount
            positions.append({'time': entry_time, 'signal': signal, 'price': entry_price, 'lot': lot, 'pnl': pnl_amount, 'balance': balance})
            
    logger.info(f"Backtest complete. Final balance: {balance:.2f}")
    if not positions:
        return pd.DataFrame()
    return pd.DataFrame(positions) 