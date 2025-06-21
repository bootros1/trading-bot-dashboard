import MetaTrader5 as mt5

login = 93863590
password = 'H@6eBsBb'
server = 'MetaQuotes-Demo'

if not mt5.initialize(login=login, password=password, server=server):
    print("MT5 login failed:", mt5.last_error())
else:
    print("✅ MT5 login successful!")
    mt5.shutdown()
