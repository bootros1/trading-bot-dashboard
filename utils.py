import os
import logging
from datetime import datetime
from config import LOG_DIR
from logging.handlers import RotatingFileHandler

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