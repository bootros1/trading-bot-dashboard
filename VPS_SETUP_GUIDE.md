# VPS Setup Guide for Forex Trading Bot

## Prerequisites
- Windows VPS from ForexVPS.net (or similar provider)
- MetaTrader 5 account credentials
- Telegram Bot Token and Chat ID (already configured)

## Step 1: Connect to Your VPS
1. Use Remote Desktop Connection (RDP) to connect to your VPS
2. Log in with your VPS credentials

## Step 2: Install Required Software

### Install Git
1. Download Git for Windows from: https://git-scm.com/download/win
2. Run the installer with default settings
3. Verify installation by opening PowerShell and typing: `git --version`

### Install Python
1. Download Python 3.9+ from: https://www.python.org/downloads/
2. **IMPORTANT**: Check "Add Python to PATH" during installation
3. Verify installation: `python --version`

### Install MetaTrader 5
1. Download MT5 from your broker's website
2. Install with default settings
3. Log in with your trading account credentials
4. Keep MT5 running in the background

## Step 3: Clone and Setup the Bot

### Clone Repository
```powershell
# Open PowerShell as Administrator
cd C:\
git clone https://github.com/bootros1/trading-bot-dashboard.git
cd trading-bot-dashboard
```

### Install Python Dependencies
```powershell
pip install -r requirements.txt
```

### Configure the Bot
1. Open `config.py` in Notepad or any text editor
2. Update these critical settings:
   ```python
   # Replace with your actual Telegram credentials
   TELEGRAM_TOKEN = 'YOUR_ACTUAL_BOT_TOKEN'
   TELEGRAM_CHAT_ID = 'YOUR_ACTUAL_CHAT_ID'
   
   # Verify your MT5 credentials
   ACCOUNT_LOGIN = 93863590
   ACCOUNT_PASSWORD = 'H@6eBsBb'
   SERVER = 'MetaQuotes-Demo'  # Change to your live server when ready
   ```

## Step 4: Test the Setup

### Test MT5 Connection
```powershell
python test_mt5_login.py
```

### Test Telegram Notifications
```powershell
python test_telegram.py
```

### Test the Bot (Optional - Run Once)
```powershell
python main.py
```

## Step 5: Automate the Bot

### Create a Batch File
Create a file called `run_bot.bat` in the project directory:
```batch
@echo off
cd /d C:\trading-bot-dashboard
python main.py
pause
```

### Set Up Windows Task Scheduler
1. Open "Task Scheduler" (search in Start menu)
2. Click "Create Basic Task"
3. Name: "Forex Trading Bot"
4. Trigger: Daily
5. Start time: Choose when you want it to start
6. Action: Start a program
7. Program: `C:\trading-bot-dashboard\run_bot.bat`
8. Finish

### Advanced Scheduling (Every 15 minutes)
1. In Task Scheduler, create a new task
2. Name: "Forex Bot - 15min"
3. Triggers tab → New Trigger
4. Begin: At startup
5. Repeat every: 15 minutes
6. Actions tab → New Action
7. Program: `python`
8. Arguments: `C:\trading-bot-dashboard\main.py`
9. Start in: `C:\trading-bot-dashboard`

## Step 6: Monitor and Maintain

### Check Logs
- Logs are stored in `C:\trading-bot-dashboard\logs\`
- Check `main.log` for bot activity
- Check `backtest_results.csv` for trade history

### Monitor Telegram
- The bot will send notifications for all trades
- You'll receive alerts for successful and failed trades

### VPS Maintenance
- Keep Windows updated
- Monitor disk space
- Ensure MT5 stays logged in
- Restart the VPS weekly if needed

## Troubleshooting

### Common Issues

**MT5 Connection Failed**
- Ensure MT5 is running and logged in
- Check account credentials in config.py
- Verify server name is correct

**Python Not Found**
- Reinstall Python with "Add to PATH" checked
- Restart PowerShell after installation

**Telegram Notifications Not Working**
- Verify bot token and chat ID
- Test with test_telegram.py script

**Bot Not Running**
- Check Windows Task Scheduler
- Verify the batch file path is correct
- Check logs for error messages

## Security Notes
- Keep your VPS credentials secure
- Don't share your Telegram bot token
- Use strong passwords for MT5 account
- Consider using a VPN for additional security

## Support
If you encounter issues:
1. Check the logs in the `logs/` directory
2. Test individual components (MT5, Telegram)
3. Verify all configuration settings
4. Restart the VPS if needed 