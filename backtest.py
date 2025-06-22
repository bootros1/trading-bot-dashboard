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
        window = df.iloc[i-51:i].copy()
        signal, atr = generate_signal(window)
        
        if signal and atr:
            price = window.iloc[-1]['close']
            sl, tp = get_sl_tp(price, signal, atr)
            
            if sl is None or tp is None:
                continue

            sl_pips = abs(price - sl) / pip_size
            tp_pips = abs(price - tp) / pip_size

            lot = calculate_position_size(balance, sl_pips)
            if lot <= 0:
                continue

            # Simulate trade outcome over the next bar
            next_bar = df.iloc[i] # The bar immediately after the signal
            pnl_pips = 0
            
            if signal == 'buy':
                if next_bar['low'] <= sl:
                    pnl_pips = -sl_pips
                elif next_bar['high'] >= tp:
                    pnl_pips = tp_pips
                else:
                    pnl_pips = (next_bar['close'] - price) / pip_size # Close at end of bar
            
            elif signal == 'sell':
                if next_bar['high'] >= sl:
                    pnl_pips = -sl_pips
                elif next_bar['low'] <= tp:
                    pnl_pips = tp_pips
                else:
                    pnl_pips = (price - next_bar['close']) / pip_size # Close at end of bar
            
            # PnL in account currency - simplified for backtesting
            # This assumes a fixed pip value, which is an approximation
            pip_value_per_lot = 10 
            pnl_amount = pnl_pips * lot * pip_value_per_lot
            balance += pnl_amount
            positions.append({'signal': signal, 'price': price, 'lot': lot, 'pnl': pnl_amount, 'balance': balance})
            
    logger.info(f"Backtest complete. Final balance: {balance:.2f}")
    return pd.DataFrame(positions) 