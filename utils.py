import os
import logging
from datetime import datetime
from config import LOG_DIR

def setup_logger(name):
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    # Remove all handlers if already present to avoid duplicate logs
    if logger.hasHandlers():
        logger.handlers.clear()
    fh = logging.FileHandler(f"{LOG_DIR}{name}.log")
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger

def format_time(ts=None):
    if ts is None:
        ts = datetime.now()
    return ts.strftime('%Y-%m-%d %H:%M:%S') 