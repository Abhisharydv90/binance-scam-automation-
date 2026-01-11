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

class TradeExecutor:
    def __init__(self):
        self.driver = DriverManager.get_driver()

    def execute_trade(self, symbol="BTCUSD", side="BUY", quantity=0.001):
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
            
            # Navigate to trading
            self.driver.get("https://academy.binance.com/en/trade")
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='trade-symbol-input']")))
            
            # Execute trade
            self.driver.find_element(By.CSS_SELECTOR, "[data-testid='trade-symbol-input']").send_keys(symbol)
            self.driver.find_element(By.CSS_SELECTOR, "[data-testid='trade-quantity-input']").send_keys(str(quantity))
            self.driver.find_element(By.CSS_SELECTOR, "[data-testid='trade-side-select']").send_keys(side)
            self.driver.find_element(By.CSS_SELECTOR, "[data-testid='trade-submit-button']").click()
            
            # Wait for trade confirmation
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='trade-success-message']")))
            return True
        except Exception as e:
            logging.error(f"Trade failed: {e}")
            return False
        finally:
            pass
