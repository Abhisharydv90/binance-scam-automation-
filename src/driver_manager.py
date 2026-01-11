from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

class DriverManager:
    @staticmethod
    def get_driver():
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")
        
        try:
            service = Service(ChromeDriverManager(version="114.0.5735.90").install())
            return webdriver.Chrome(service=service, options=options)
        except Exception as e:
            try:
                service = Service("/usr/bin/chromedriver")
                return webdriver.Chrome(service=service, options=options)
            except:
                raise Exception(f"Failed to initialize ChromeDriver: {e}")
