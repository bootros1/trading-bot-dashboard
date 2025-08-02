import os
import logging
from datetime import datetime
from config import LOG_DIR
from logging.handlers import RotatingFileHandler
import csv

def setup_logger(name, log_file='logs/main.log', level=logging.INFO):
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=5)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    # Prevent duplicate handlers
    if not any(isinstance(h, RotatingFileHandler) and h.baseFilename == handler.baseFilename for h in logger.handlers):
        logger.addHandler(handler)
    return logger

def format_time(ts=None):
    if ts is None:
        ts = datetime.now()
    return ts.strftime('%Y-%m-%d %H:%M:%S')

def log_trade(trade_data):
    """
    Appends a trade record to logs/trades.csv. Creates the file with headers if it doesn't exist.
    Expects trade_data to be a dict with keys:
    timestamp, symbol, direction, lot, entry, sl, tp, result, error, pnl, balance
    """
    log_file = os.path.join(LOG_DIR, 'trades.csv')
    fieldnames = ['timestamp', 'symbol', 'direction', 'lot', 'entry', 'sl', 'tp', 'result', 'error', 'pnl', 'balance']
    file_exists = os.path.isfile(log_file)
    with open(log_file, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({k: trade_data.get(k, '') for k in fieldnames}) 