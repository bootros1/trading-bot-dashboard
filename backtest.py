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

    for i in range(51, len(df)): # Start after enough data for indicators
        window = df.iloc[i-51:i].copy()
        signal, atr = generate_signal(window)
        
        if signal and atr:
            price = window.iloc[-1]['close']
            sl, tp = get_sl_tp(price, signal, atr)
            
            if sl is None:
                continue

            sl_pips = abs(price - sl) / pip_size
            lot = calculate_position_size(balance, sl_pips)

            # Simulate trade outcome over the next bar
            bar = df.iloc[i] # The bar immediately after the signal
            pnl = 0
            
            if signal == 'buy':
                if bar['low'] <= sl:
                    pnl = -sl_pips
                elif bar['high'] >= tp:
                    pnl = abs(tp - price) / pip_size
            else: # 'sell'
                if bar['high'] >= sl:
                    pnl = -sl_pips
                elif bar['low'] <= tp:
                    pnl = abs(price - tp) / pip_size
            
            # PnL in account currency
            pnl_amount = pnl * lot * 10 # Assuming $10 per pip per standard lot
            balance += pnl_amount
            positions.append({'signal': signal, 'price': price, 'lot': lot, 'pnl': pnl_amount, 'balance': balance})
            
    logger.info(f"Backtest complete. Final balance: {balance:.2f}")
    return pd.DataFrame(positions) 