import importlib.util
import os

notifier_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notifier.py")
spec = importlib.util.spec_from_file_location("notifier", notifier_path)
notifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(notifier)

notifier.send_telegram("🚀 Test: Your Forex bot is ready to trade!")
 
send_telegram("🚀 Test: Your Forex bot is ready to trade!") 