# Automated Trading Bot

A Python-based automated trading bot that executes trades based on technical indicators (RSI + Moving Average crossover strategy) with built-in risk management and multi-broker support.

## What the Bot Does

- **Strategy**: RSI + MA Crossover (RSI oversold/overbought + MA20/MA50 crossover)
- **Risk Management**: Dynamic position sizing, ATR-based stop-loss, 1.5:1 reward/risk ratio
- **Automation**: 24/7 automated trading with Windows Task Scheduler
- **Notifications**: Telegram alerts for trade execution and status updates
- **Multi-Broker**: Seamlessly switch between forex and crypto trading

## Supported Brokers

### OANDA (Forex)
- Demo and live account support
- REST API integration via `oandapyV20`
- Forex pairs: EUR/USD, GBP/USD, USD/CAD, etc.
- Risk management with pip-based calculations

### Kraken (Crypto)
- Live crypto trading via `ccxt` library
- 20+ popular crypto pairs: BTC/USD, ETH/USD, 1INCH/USD, etc.
- Real-time market data and order execution
- Advanced position sizing for crypto volatility

## Setup Instructions

### Requirements
- **Python**: 3.8 or higher
- **OS**: Windows (for Task Scheduler automation)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Forex
   ```

2. **Install Python packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create logs directory**:
   ```bash
   mkdir logs
   ```

### Configuration

1. **Set up environment variables** (recommended for security):
   
   Copy the example file and add your credentials:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your actual credentials:
   ```bash
   # OANDA Configuration
   OANDA_API_KEY=your_oanda_api_key_here
   OANDA_ACCOUNT_ID=your_oanda_account_id_here
   
   # Kraken Configuration  
   KRAKEN_API_KEY=your_kraken_api_key_here
   KRAKEN_API_SECRET=your_kraken_api_secret_here
   
   # Telegram Configuration
   TELEGRAM_TOKEN=your_telegram_bot_token_here
   TELEGRAM_CHAT_ID=your_telegram_chat_id_here
   
   # Select broker
   BROKER=KRAKEN
   ```
   
   **Important**: Never commit your `.env` file to version control!
   
   **Alternative**: You can still edit `config.py` directly, but using environment variables is more secure.

2. **Set up Telegram bot** (optional):
   - Create bot via @BotFather
   - Get chat ID from @userinfobot
   - Add token and chat ID to config

## How to Run Tests

### Test Broker Connections
```bash
python test_multi_broker.py
```

### Test OANDA Setup
```bash
python test_oanda.py
```

### Test Kraken Setup
```bash
python test_kraken.py
```

### Test Live Trade (OANDA)
```bash
python live_trade_test.py
```

### Test Crypto Trade (Kraken)
```bash
python test_crypto_trade.py
```

### Scan for Trading Signals
```bash
python test_extended_crypto_pairs.py
```

### Run Backtesting
```bash
python backtest.py
```

## Running the Bot

### Manual Execution
```bash
python main.py
```

### Automated Trading (Windows)
```bash
python scheduler.py
```

This creates a Windows scheduled task that runs the bot daily at 9:00 AM.

## Key Features

- **Multi-Broker Architecture**: Unified interface for OANDA and Kraken
- **Risk Management**: Position sizing, stop-loss, take-profit automation
- **Signal Generation**: RSI + MA crossover strategy
- **Real-time Monitoring**: Telegram notifications for all trades
- **Error Handling**: Comprehensive logging and error recovery
- **Scalable**: Easy to add new brokers and strategies

## File Structure

```
Forex/
├── main.py                 # Main trading bot
├── strategy.py             # RSI + MA strategy
├── risk.py                 # Position sizing & risk management
├── config.py               # Configuration settings
├── trader_interface.py     # Multi-broker interface
├── oanda_broker.py         # OANDA integration
├── kraken_client.py        # Kraken integration
├── utils.py                # Logging utilities
├── backtest.py             # Strategy backtesting
├── scheduler.py            # Windows task automation
├── logs/                   # Trading logs
└── requirements.txt        # Python dependencies
```

## Recent Success

✅ **Successfully executed live trades**:
- 1INCH/USD: BUY @ $0.2451 (163.33 units)
- STORJ/USD: BUY @ $0.2602 (9.53 units)

Both trades include automatic stop-loss and take-profit management.