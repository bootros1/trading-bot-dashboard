#!/usr/bin/env python3
"""
Windows Task Scheduler setup for automated trading bot.
"""

import os
import sys
import subprocess
from datetime import datetime

def create_scheduled_task():
    """Create a Windows scheduled task to run the trading bot daily."""
    
    # Get current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    python_path = sys.executable
    script_path = os.path.join(current_dir, 'main.py')
    
    # Task name and description
    task_name = "TradingBot"
    task_description = "Automated Forex/Crypto Trading Bot"
    
    # Create the command
    command = f'"{python_path}" "{script_path}"'
    
    # Create the scheduled task
    schtasks_cmd = [
        'schtasks', '/create', '/tn', task_name,
        '/tr', command,
        '/sc', 'daily',
        '/st', '09:00',
        '/f',  # Force overwrite if exists
        '/ru', 'SYSTEM',  # Run as SYSTEM
        '/rl', 'HIGHEST',  # Highest privileges
        '/it',  # Interactive task
        '/np'   # No password
    ]
    
    print("🔧 Setting up Windows Task Scheduler...")
    print(f"Task Name: {task_name}")
    print(f"Command: {command}")
    print(f"Schedule: Daily at 09:00")
    
    try:
        # Create the scheduled task
        result = subprocess.run(schtasks_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Scheduled task created successfully!")
            print("📅 The trading bot will run daily at 09:00")
            return True
        else:
            print(f"❌ Failed to create scheduled task:")
            print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating scheduled task: {e}")
        return False

def list_scheduled_tasks():
    """List existing scheduled tasks."""
    try:
        result = subprocess.run(['schtasks', '/query', '/tn', 'TradingBot'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("📋 Current TradingBot task:")
            print(result.stdout)
        else:
            print("ℹ️  No TradingBot task found")
            
    except Exception as e:
        print(f"❌ Error listing tasks: {e}")

def delete_scheduled_task():
    """Delete the scheduled task."""
    try:
        result = subprocess.run(['schtasks', '/delete', '/tn', 'TradingBot', '/f'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Scheduled task deleted successfully!")
        else:
            print(f"❌ Failed to delete task: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Error deleting task: {e}")

def create_batch_file():
    """Create a batch file to run the trading bot."""
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    python_path = sys.executable
    script_path = os.path.join(current_dir, 'main.py')
    
    batch_content = f'''@echo off
cd /d "{current_dir}"
echo Starting Trading Bot at %date% %time%
"{python_path}" "{script_path}"
pause
'''
    
    batch_file = os.path.join(current_dir, 'run_trading_bot.bat')
    
    try:
        with open(batch_file, 'w') as f:
            f.write(batch_content)
        
        print(f"✅ Batch file created: {batch_file}")
        print("💡 You can double-click this file to run the bot manually")
        return True
        
    except Exception as e:
        print(f"❌ Error creating batch file: {e}")
        return False

def main():
    """Main function to set up automation."""
    print("🤖 Trading Bot Automation Setup")
    print("=" * 50)
    
    while True:
        print("\nOptions:")
        print("1. Create scheduled task (daily at 09:00)")
        print("2. List current tasks")
        print("3. Delete scheduled task")
        print("4. Create batch file for manual execution")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == '1':
            create_scheduled_task()
        elif choice == '2':
            list_scheduled_tasks()
        elif choice == '3':
            delete_scheduled_task()
        elif choice == '4':
            create_batch_file()
        elif choice == '5':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 