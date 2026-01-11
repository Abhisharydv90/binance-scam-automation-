from src.driver_manager import DriverManager
import time
import logging
from dotenv import load_dotenv
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()
logging.basicConfig(level=logging.INFO if os.getenv("DEBUG") else logging.WARNING)

class ProfitMonitor:
    def __init__(self):
        self.driver = DriverManager.get_driver()

    def monitor_profit(self):
        try:
            self.driver.get("https://academy.binance.com/en/login")
            wait = WebDriverWait(self.driver, 30)
            
            # Login
            email_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='email-input']")))
            email_field.send_keys(os.getenv("EMAIL"))
            self.driver.find_element(By.CSS_SELECTOR, "[data-testid='password-input']").send_keys(os.getenv("PASSWORD"))
            self.driver.find_element(By.CSS_SELECTOR, "[data-testid='login-button']").click()
            
            # Wait for dashboard
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='dashboard-header']")))
            
            # Check profit
            profit_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='profit-display']")))
            balance = float(profit_element.text.replace("₹", "").replace(",", ""))
            
            if balance > float(os.getenv("WITHDRAW_THRESHOLD")):
                self.withdraw_profit(balance)
                
            return balance
        except Exception as e:
            logging.error(f"Profit check failed: {e}")
            return 0
        finally:
            pass

    def withdraw_profit(self, amount):
        try:
            self.driver.get("https://academy.binance.com/en/withdraw")
            wait = WebDriverWait(self.driver, 30)
            
            # Wait for withdrawal form
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='amount-input']")))
            
            # Withdraw funds
            self.driver.find_element(By.CSS_SELECTOR, "[data-testid='amount-input']").send_keys(str(amount))
            self.driver.find_element(By.CSS_SELECTOR, "[data-testid='withdraw-button']").click()
            
            # Wait for success message
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='withdraw-success-message']")))
            logging.info(f"Withdrawn ₹{amount:,}")
        except Exception as e:
            logging.error(f"Withdrawal failed: {e}")
