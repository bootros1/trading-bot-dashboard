import MetaTrader5 as mt5
from config import ACCOUNT_LOGIN, ACCOUNT_PASSWORD, SERVER

# --- Filter Settings ---
# Set the maximum allowed spread in points. 10 points = 1 pip for 5-digit brokers.
MAX_SPREAD = 20
# Only include symbols that are forex pairs (as classified by the broker)
ONLY_FOREX = True
# Only include symbols containing these currencies (e.g., only majors). Leave empty to include all.
# Example: INCLUDE_CURRENCIES = ['USD', 'EUR', 'GBP', 'JPY']
INCLUDE_CURRENCIES = []


def connect_mt5():
    """Connects to the MetaTrader 5 terminal."""
    if not mt5.initialize(login=ACCOUNT_LOGIN, password=ACCOUNT_PASSWORD, server=SERVER):
        print(f"MT5 initialize() failed, error code: {mt5.last_error()}")
        return False
    print("✅ MT5 connection successful!")
    return True


def scan_symbols():
    """Scans for symbols based on the filter settings and returns a list."""
    all_symbols = mt5.symbols_get()
    if not all_symbols:
        print("No symbols found. Make sure you are connected.")
        return []

    print(f"Scanning {len(all_symbols)} total symbols from the broker...")
    filtered_symbols = []

    for symbol in all_symbols:
        # We need to get the full symbol information
        info = mt5.symbol_info(symbol.name)
        if not info:
            continue

        # --- Apply Filters ---
        # 1. Check if the symbol is visible in Market Watch (tradable)
        if not info.visible:
            continue

        # 2. Check spread
        # The spread is in points, convert to pips if needed
        if info.spread > MAX_SPREAD:
            continue
            
        # 3. Check if it's a forex pair
        if ONLY_FOREX and 'forex' not in info.path.lower():
            continue

        # 4. Check for specific currencies
        if INCLUDE_CURRENCIES:
            if not any(curr in info.name for curr in INCLUDE_CURRENCIES):
                continue
        
        filtered_symbols.append(info.name)

    return filtered_symbols


def main():
    """Main function to run the scanner."""
    if not connect_mt5():
        return

    tradable_symbols = scan_symbols()
    mt5.shutdown()

    if tradable_symbols:
        print("\n--- Found Tradable Symbols ---")
        print(f"{len(tradable_symbols)} symbols match your criteria.")
        print("\nYou can copy this Python list into your other scripts:")
        print(f"\nSYMBOLS = {tradable_symbols}")
    else:
        print("\n--- No symbols matched your filter criteria. ---")
        print("Try adjusting the MAX_SPREAD or other settings in this script.")


if __name__ == '__main__':
    main() 