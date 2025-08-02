# OANDA Trading Bot Setup Guide

## Overview
This guide helps you transition your trading bot from MetaTrader 5 to OANDA's REST API.

## Prerequisites

### 1. OANDA Account Setup
1. **Create OANDA Account:**
   - Go to [OANDA.com](https://www.oanda.com)
   - Sign up for a demo account (free)
   - Complete the registration process

2. **Get API Credentials:**
   - Log into your OANDA account
   - Go to "My Account" → "API Access"
   - Generate a new API key
   - Note your Account ID (found in account details)

### 2. Install Required Packages
```bash
pip install -r requirements.txt
```

## Configuration

### 1. Update `config.py`
Replace the placeholder values with your actual OANDA credentials:

```python
# OANDA Configuration (Demo Environment)
OANDA_API_KEY = 'your_actual_oanda_api_key_here'
OANDA_ACCOUNT_ID = 'your_actual_oanda_account_id_here'
OANDA_ENVIRONMENT = 'practice'  # 'practice' for demo, 'live' for live trading
```

### 2. Symbol Format
OANDA uses different symbol formats than MT5:
- **MT5:** EURUSD, GBPUSD
- **OANDA:** EUR_USD, GBP_USD

The symbols are already updated in `config.py`.

## Testing the Connection

### 1. Test OANDA Connection
Create a test script to verify your connection:

```python
from oanda_broker import initialize_broker, get_broker

# Test connection
if initialize_broker():
    broker = get_broker()
    account_info = broker.get_account_info()
    if account_info:
        print(f"✅ Connected to OANDA!")
        print(f"Balance: {account_info['balance']} {account_info['currency']}")
    else:
        print("❌ Failed to get account info")
else:
    print("❌ Failed to connect to OANDA")
```

### 2. Test Historical Data
```python
from oanda_broker import initialize_broker, get_broker

broker = get_broker()
if broker:
    df = broker.get_historical_data('EUR_USD', 'M15', bars=10)
    if df is not None:
        print(f"✅ Historical data retrieved: {len(df)} bars")
        print(df.head())
    else:
        print("❌ Failed to get historical data")
```

## Running the Bot

### 1. Demo Mode (Recommended First)
```bash
python main.py
```

### 2. Monitor Logs
Check the `logs/` directory for:
- `main.log` - Main bot activity
- `oanda_broker.log` - OANDA API interactions

### 3. Telegram Notifications
The bot will send Telegram notifications for:
- ✅ Successful trades
- ❌ Failed trades
- 📊 Account updates

## Key Differences from MT5

### 1. Units vs Lots
- **MT5:** Uses lot sizes (0.01, 0.1, 1.0)
- **OANDA:** Uses units (1000, 10000, 100000)
- **Conversion:** 1 lot = 100,000 units

### 2. Order Types
- **MT5:** Market orders with filling modes
- **OANDA:** Market orders with FOK (Fill or Kill)

### 3. Price Data
- **MT5:** Bid/Ask prices
- **OANDA:** Mid prices (average of bid/ask)

## Troubleshooting

### Common Issues

1. **API Key Error:**
   - Verify your API key is correct
   - Ensure you're using the demo environment for testing

2. **Account ID Error:**
   - Check your Account ID in OANDA account settings
   - Make sure you're using the correct account

3. **Symbol Not Found:**
   - Verify symbol format (EUR_USD, not EURUSD)
   - Check if the symbol is available in your account

4. **Insufficient Funds:**
   - Start with minimum units (1000 = 0.01 lot)
   - Check your account balance

### Error Messages

- `"Invalid API key"` → Check your API key
- `"Account not found"` → Verify Account ID
- `"Instrument not found"` → Check symbol format
- `"Insufficient margin"` → Reduce position size

## Live Trading Setup

### 1. Switch to Live Environment
When ready for live trading:

```python
# In config.py
OANDA_ENVIRONMENT = 'live'  # Change from 'practice' to 'live'
OANDA_BASE_URL = 'https://api-fxtrade.oanda.com'  # Live environment
```

### 2. Update API Key
- Generate a new API key for live trading
- Update `OANDA_API_KEY` in `config.py`

### 3. Test with Small Amounts
- Start with minimum position sizes
- Monitor closely for the first few trades

## Security Best Practices

1. **Never share your API key**
2. **Use environment variables for production**
3. **Regularly rotate API keys**
4. **Monitor account activity**
5. **Set up account alerts**

## Support

- **OANDA API Documentation:** https://developer.oanda.com/
- **OANDA Support:** Contact OANDA customer service
- **Bot Issues:** Check logs in `logs/` directory

## Migration Checklist

- [ ] Create OANDA demo account
- [ ] Get API key and Account ID
- [ ] Update `config.py` with credentials
- [ ] Install required packages
- [ ] Test connection
- [ ] Test historical data retrieval
- [ ] Run bot in demo mode
- [ ] Monitor logs and Telegram notifications
- [ ] Verify trade execution
- [ ] Switch to live trading (when ready) 