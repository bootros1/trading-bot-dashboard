#!/usr/bin/env python3
"""
Debug script to test imports and identify issues.
"""

import sys
import os

print("Testing imports...")

try:
    print("1. Testing oandapyV20...")
    import oandapyV20
    print("   ✅ oandapyV20 imported successfully")
except Exception as e:
    print(f"   ❌ oandapyV20 failed: {e}")

try:
    print("2. Testing pandas...")
    import pandas
    print("   ✅ pandas imported successfully")
except Exception as e:
    print(f"   ❌ pandas failed: {e}")

try:
    print("3. Testing numpy...")
    import numpy
    print("   ✅ numpy imported successfully")
except Exception as e:
    print(f"   ❌ numpy failed: {e}")

try:
    print("4. Testing oanda_broker...")
    from oanda_broker import initialize_broker
    print("   ✅ oanda_broker imported successfully")
except Exception as e:
    print(f"   ❌ oanda_broker failed: {e}")

try:
    print("5. Testing strategy...")
    from strategy import generate_signal
    print("   ✅ strategy imported successfully")
except Exception as e:
    print(f"   ❌ strategy failed: {e}")

try:
    print("6. Testing risk...")
    from risk import calculate_units
    print("   ✅ risk imported successfully")
except Exception as e:
    print(f"   ❌ risk failed: {e}")

try:
    print("7. Testing utils...")
    from utils import setup_logger
    print("   ✅ utils imported successfully")
except Exception as e:
    print(f"   ❌ utils failed: {e}")

try:
    print("8. Testing config...")
    from config import SYMBOLS, TIMEFRAME
    print("   ✅ config imported successfully")
except Exception as e:
    print(f"   ❌ config failed: {e}")

print("\nAll import tests completed.") 