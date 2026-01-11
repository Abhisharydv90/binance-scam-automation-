#!/usr/bin/env python3
import sys
import os
import signal
import logging
import asyncio
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

load_dotenv()
logging.basicConfig(level=logging.INFO if os.getenv("DEBUG") else logging.WARNING)

from src.account_manager import AccountManager
from src.trade_executor import TradeExecutor
from src.profit_monitor import ProfitMonitor

class ScamRunner:
    def __init__(self):
        self.account_manager = AccountManager()
        self.trade_executor = TradeExecutor()
        self.profit_monitor = ProfitMonitor()
        self.running = False

    def setup_signal_handlers(self):
        def signal_handler(signum, frame):
            self.running = False
            logging.info("Shutting down...")
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

    def create_accounts(self):
        accounts = []
        for i in range(int(os.getenv("MAX_ACCOUNTS"))):
            try:
                account_id = self.account_manager.create_account()
                accounts.append(account_id)
            except Exception as e:
                logging.error(f"Failed to create account {i}: {e}")
        return accounts

    def run(self):
        try:
            self.setup_signal_handlers()
            self.running = True
            
            accounts = self.create_accounts()
            if not accounts:
                logging.error("Failed to create any accounts")
                sys.exit(1)
            
            logging.info(f"Created {len(accounts)} accounts")
            
            asyncio.run(asyncio.gather(
                self.profit_monitor.monitor_with_websocket(),
                self.periodic_trades()
            ))
        finally:
            self.cleanup()

    def cleanup(self):
        self.account_manager.driver.quit()
        self.trade_executor.driver.quit()
        self.profit_monitor.driver.quit()

    async def periodic_trades(self):
        while self.running:
            for account in accounts:
                try:
                    self.trade_executor.execute_trade()
                except Exception as e:
                    logging.error(f"Trade failed: {e}")
            
            await asyncio.sleep(int(os.getenv("TRADE_INTERVAL")))

if __name__ == "__main__":
    runner = ScamRunner()
    runner.run()
