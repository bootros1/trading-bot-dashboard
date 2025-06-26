import os
import sys

# Add current directory to Python path for local imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

LOCK_FILE = 'bot.lock'

# Atomic lock: prevent multiple instances
if os.path.exists(LOCK_FILE):
    print('Another instance of the bot is already running. Exiting.')
    sys.exit(1)

with open(LOCK_FILE, 'w') as f:
    f.write('locked')

import atexit

def remove_lock():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

atexit.register(remove_lock)

try:
    from broker import connect, disconnect, get_account_info, get_historical_data, place_order
    from strategy import generate_signal
    from risk import calculate_lot_size, get_sl_tp
    from utils import setup_logger, log_trade
    from config import SYMBOLS, TIMEFRAME, ATR_SL_MULTIPLIER, BACKTEST, INITIAL_BALANCE
    from backtest import run_backtest
    import pandas as pd
    from datetime import datetime

    logger = setup_logger('main')

    def live_trading():
        """Scans multiple symbols and executes a trade on the first valid signal."""
        if not connect():
            return

        info = get_account_info()
        if info is None:
            disconnect()
            return
        
        balance = info.balance
        trade_executed = False

        logger.info(f"Scanning {len(SYMBOLS)} symbols for a signal...")

        for symbol in SYMBOLS:
            logger.info(f"--- Analyzing {symbol} ---")
            df = get_historical_data(symbol, TIMEFRAME, bars=100)
            if df is None or df.empty:
                logger.warning(f"Could not get historical data for {symbol}. Skipping.")
                continue

            signal, atr = generate_signal(df)
            if signal and atr:
                logger.info(f"Signal FOUND for {symbol}: {signal.upper()}, ATR: {atr:.5f}")
                
                # Convert ATR to pips for position sizing
                pip_size = 0.0001  # For 5-digit brokers
                sl_pips = (atr * ATR_SL_MULTIPLIER) / pip_size

                price = df.iloc[-1]['close']
                lot = calculate_lot_size(balance, sl_pips)
                sl, tp = get_sl_tp(price, signal, atr)
                
                if lot > 0.0 and sl is not None:
                    success = place_order(symbol, signal, lot, sl, tp)
                    if success:
                        logger.info(f"Trade executed for {symbol}: {signal} {lot} lots at {price}, SL: {sl:.5f}, TP: {tp:.5f}")
                        trade_executed = True
                        trade_data = {
                            'timestamp': datetime.now().isoformat(),
                            'symbol': symbol,
                            'direction': signal,
                            'lot': lot,
                            'entry': price,
                            'sl': sl,
                            'tp': tp,
                            'result': 'executed',
                            'error': '',
                            'pnl': 0,  # Placeholder for now
                            'balance': balance  # Current balance after trade
                        }
                        log_trade(trade_data)
                        break  # Stop scanning after one successful trade
                    else:
                        logger.error(f"Failed to place order for {symbol}. Will continue scanning.")
                else:
                    logger.warning(f"Could not calculate valid lot size or SL/TP for {symbol}. Skipping trade.")
            else:
                logger.info(f"No signal for {symbol}.")

        if not trade_executed:
            logger.info("Scan complete. No valid trading signals found on any symbol today.")

        disconnect()

    def run_full_backtest():
        """
        Runs a backtest across all symbols defined in the config and combines the results.
        """
        logger.info("--- Starting Full Multi-Symbol Backtest ---")
        all_results = []
        
        for symbol in SYMBOLS:
            file_path = f'historical_{symbol}_{TIMEFRAME}.csv'
            logger.info(f"Loading data for {symbol} from {file_path}...")
            
            try:
                df = pd.read_csv(file_path)
                if df.empty:
                    logger.warning(f"Data file for {symbol} is empty. Skipping.")
                    continue
            except FileNotFoundError:
                logger.warning(f"Historical data file not found for {symbol} at {file_path}. Skipping.")
                continue
            
            # We need to add the symbol to the results to differentiate trades
            symbol_results = run_backtest(df, initial_balance=INITIAL_BALANCE)
            if not symbol_results.empty:
                symbol_results['symbol'] = symbol
                all_results.append(symbol_results)

        if not all_results:
            logger.error("No trades were generated across any symbols. Backtest results file will be empty.")
            # Create an empty file with headers so the dashboard doesn't error out on file-not-found
            pd.DataFrame(columns=['signal', 'price', 'lot', 'pnl', 'balance', 'symbol']).to_csv('logs/backtest_results.csv', index=False)
            return

        # Combine all results and sort by the trade execution order (index)
        final_results = pd.concat(all_results).sort_index().reset_index(drop=True)
        
        # Recalculate the balance column to be cumulative across all trades
        final_results['balance'] = INITIAL_BALANCE + final_results['pnl'].cumsum()

        final_results.to_csv('logs/backtest_results.csv', index=False)
        logger.info(f"--- Full Backtest Complete ---")
        logger.info(f"Results for {len(final_results)} trades across {len(SYMBOLS)} symbols saved to logs/backtest_results.csv")

    def main():
        if BACKTEST:
            run_full_backtest()
        else:
            live_trading()

    if __name__ == '__main__':
        main()
except Exception as e:
    print(f'Error: {e}')
    remove_lock()
    raise 