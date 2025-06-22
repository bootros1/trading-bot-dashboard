# Forex Trading Bot Status Checker
# Run this script to check the bot's status and recent activity

Write-Host "=== Forex Trading Bot Status Check ===" -ForegroundColor Green
Write-Host "Time: $(Get-Date)" -ForegroundColor Gray
Write-Host ""

# Check if we're in the right directory
if (!(Test-Path "config.py")) {
    Write-Host "ERROR: config.py not found. Please run this script from the bot directory." -ForegroundColor Red
    pause
    exit 1
}

# Check if logs directory exists
if (!(Test-Path "logs")) {
    Write-Host "⚠ No logs directory found. Bot may not have run yet." -ForegroundColor Yellow
} else {
    # Check main log file
    $logFile = "logs\main.log"
    if (Test-Path $logFile) {
        Write-Host "=== Recent Log Entries ===" -ForegroundColor Cyan
        $recentLogs = Get-Content $logFile -Tail 10
        foreach ($line in $recentLogs) {
            Write-Host $line -ForegroundColor White
        }
        Write-Host ""
    } else {
        Write-Host "⚠ No main.log file found. Bot may not have run yet." -ForegroundColor Yellow
    }
    
    # Check backtest results
    $resultsFile = "logs\backtest_results.csv"
    if (Test-Path $resultsFile) {
        Write-Host "=== Backtest Results ===" -ForegroundColor Cyan
        $results = Import-Csv $resultsFile
        $totalTrades = $results.Count
        $winningTrades = ($results | Where-Object { $_.pnl -gt 0 }).Count
        $totalPnL = ($results | Measure-Object -Property pnl -Sum).Sum
        
        Write-Host "Total Trades: $totalTrades" -ForegroundColor White
        Write-Host "Winning Trades: $winningTrades" -ForegroundColor White
        Write-Host "Win Rate: $([math]::Round(($winningTrades / $totalTrades) * 100, 2))%" -ForegroundColor White
        Write-Host "Total PnL: $([math]::Round($totalPnL, 2))" -ForegroundColor White
        Write-Host ""
    }
}

# Check if Python processes are running
Write-Host "=== Running Processes ===" -ForegroundColor Cyan
$pythonProcesses = Get-Process python -ErrorAction SilentlyContinue
if ($pythonProcesses) {
    foreach ($proc in $pythonProcesses) {
        Write-Host "Python Process ID: $($proc.Id) - Started: $($proc.StartTime)" -ForegroundColor White
    }
} else {
    Write-Host "No Python processes currently running" -ForegroundColor Gray
}

# Check MT5 connection
Write-Host ""
Write-Host "=== MT5 Connection Test ===" -ForegroundColor Cyan
try {
    $result = python test_mt5_login.py 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ MT5 connection successful" -ForegroundColor Green
    } else {
        Write-Host "✗ MT5 connection failed" -ForegroundColor Red
        Write-Host $result -ForegroundColor Red
    }
} catch {
    Write-Host "✗ Could not test MT5 connection" -ForegroundColor Red
}

# Check Telegram
Write-Host ""
Write-Host "=== Telegram Test ===" -ForegroundColor Cyan
try {
    $result = python test_telegram.py 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Telegram notification test successful" -ForegroundColor Green
    } else {
        Write-Host "✗ Telegram notification test failed" -ForegroundColor Red
        Write-Host $result -ForegroundColor Red
    }
} catch {
    Write-Host "✗ Could not test Telegram notifications" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== Status Check Complete ===" -ForegroundColor Green
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 