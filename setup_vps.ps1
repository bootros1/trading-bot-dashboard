# Forex Trading Bot VPS Setup Script
# Run this script as Administrator on your VPS

Write-Host "=== Forex Trading Bot VPS Setup ===" -ForegroundColor Green
Write-Host ""

# Check if running as Administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "ERROR: This script must be run as Administrator" -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    pause
    exit 1
}

# Check if Git is installed
Write-Host "Checking Git installation..." -ForegroundColor Yellow
try {
    $gitVersion = git --version
    Write-Host "✓ Git found: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Git not found. Please install Git for Windows first." -ForegroundColor Red
    Write-Host "Download from: https://git-scm.com/download/win" -ForegroundColor Yellow
    pause
    exit 1
}

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.9+ first." -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Yellow
    pause
    exit 1
}

# Clone repository if not exists
$projectPath = "C:\trading-bot-dashboard"
if (Test-Path $projectPath) {
    Write-Host "Project directory already exists. Updating..." -ForegroundColor Yellow
    Set-Location $projectPath
    git pull
} else {
    Write-Host "Cloning repository..." -ForegroundColor Yellow
    Set-Location C:\
    git clone https://github.com/bootros1/trading-bot-dashboard.git
    Set-Location $projectPath
}

# Install Python dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
try {
    pip install -r requirements.txt
    Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    pause
    exit 1
}

# Create logs directory
if (!(Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs"
    Write-Host "✓ Created logs directory" -ForegroundColor Green
}

# Check if config.py needs Telegram credentials
Write-Host "Checking configuration..." -ForegroundColor Yellow
$configContent = Get-Content "config.py" -Raw
if ($configContent -match "YOUR_TELEGRAM_BOT_TOKEN") {
    Write-Host "⚠ WARNING: Telegram credentials not configured" -ForegroundColor Yellow
    Write-Host "Please update config.py with your actual Telegram bot token and chat ID" -ForegroundColor Yellow
} else {
    Write-Host "✓ Configuration appears to be set up" -ForegroundColor Green
}

Write-Host ""
Write-Host "=== Setup Complete ===" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Install MetaTrader 5 and log in" -ForegroundColor White
Write-Host "2. Update config.py with your Telegram credentials" -ForegroundColor White
Write-Host "3. Test the setup with: python test_mt5_login.py" -ForegroundColor White
Write-Host "4. Test Telegram with: python test_telegram.py" -ForegroundColor White
Write-Host "5. Run the bot with: python main.py" -ForegroundColor White
Write-Host "6. Set up Task Scheduler for automation" -ForegroundColor White
Write-Host ""
Write-Host "See VPS_SETUP_GUIDE.md for detailed instructions" -ForegroundColor Cyan
Write-Host ""
pause 