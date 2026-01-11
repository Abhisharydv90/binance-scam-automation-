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

class AccountManager:
    def __init__(self):
        self.driver = DriverManager.get_driver()

    def create_account(self):
        try:
            self.driver.get("https://academy.binance.com/en/register")
            wait = WebDriverWait(self.driver, 30)
            
            # Find and interact with form elements
            email_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='email-input']")))
            email_field.send_keys(f"user_{int(time.time())}@example.com")
            
            self.driver.find_element(By.CSS_SELECTOR, "[data-testid='password-input']").send_keys(os.getenv("PASSWORD"))
            self.driver.find_element(By.CSS_SELECTOR, "[data-testid='country-select']").send_keys("US")
            self.driver.find_element(By.CSS_SELECTOR, "[data-testid='register-button']").click()
            
            # Wait for successful registration
            wait.until(EC.url_contains("/dashboard"))
            return self.driver.current_url.split("/")[-1]
        except Exception as e:
            logging.error(f"Account creation failed: {e}")
            raise
        finally:
            pass
