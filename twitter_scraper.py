from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pymongo
from datetime import datetime, timezone
import os
from dotenv import load_dotenv
import random
import requests
import uuid
import time

class XScraper:
    def __init__(self):
        load_dotenv()
        # MongoDB setup
        self.mongodb_client = pymongo.MongoClient(os.getenv('MONGODB_URI'))
        self.db = self.mongodb_client['x_trends']
        self.collection = self.db['trends']
        
        # X credentials
        self.x_username = os.getenv('X_USERNAME')
        self.x_password = os.getenv('X_PASSWORD')
        
        # ProxyMesh Configuration
        self.proxymesh_username = os.getenv('PROXYMESH_USERNAME')
        self.proxymesh_password = os.getenv('PROXYMESH_PASSWORD')
        self.proxy_server = 'us-ca.proxymesh.com:31280'
        
        # Initialize driver as None
        self.driver = None
        
        print(f"\nCurrent Date and Time (UTC): {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Current User's Login: {self.x_username}\n")

    def setup_driver(self):
        """Set up Chrome driver with proxy configuration"""
        if self.driver:
            return self.driver
            
        try:
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--window-size=1920,1080')
            
            # Add proxy configuration
            chrome_options.add_argument(f'--proxy-server=http://{self.proxy_server}')
            chrome_options.add_argument(f'--proxy-auth={self.proxymesh_username}:{self.proxymesh_password}')
            
            # Anti-detection measures
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            self.driver = webdriver.Chrome(options=chrome_options)
            return self.driver
            
        except Exception as e:
            print(f"❌ Failed to set up driver: {str(e)}")
            return None

    def cleanup_driver(self):
        """Clean up the driver instance"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            finally:
                self.driver = None



 

    def login_to_x(self, driver):
        """Handle the X (Twitter) login process"""
        try:
            print(f"Starting login process at {datetime.now(timezone.utc)}")
            driver.get("https://x.com/login")
            time.sleep(4)  # Wait for page load

            # Enter username and press Enter
            print("Locating username field...")
            username_field = driver.find_element(By.XPATH, "//input[@name='text']")
            print(f"Entering username: {self.x_username}")
            username_field.send_keys(self.x_username)
            username_field.send_keys(Keys.RETURN)
            time.sleep(4)  # Wait for email field

            # Enter email and press Enter
            print("Entering email...")
            email_field = driver.find_element(By.CSS_SELECTOR, 'input[data-testid="ocfEnterTextTextInput"]')
            email_field.send_keys(os.getenv('USER_EMAIL'))
            email_field.send_keys(Keys.RETURN)
            time.sleep(4)  # Wait for password field

            # Enter password and press Enter
            print("Entering password...")
            password_field = driver.find_element(By.XPATH, "//input[@name='password']")
            password_field.send_keys(self.x_password)
            password_field.send_keys(Keys.RETURN)
            time.sleep(5)  # Wait for login to complete

            # Verify login success by checking for home feed
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Home')]"))
                )
                print("Successfully logged in")
                return True
            except Exception as e:
                print(f"Login verification failed: {str(e)}")
                self.take_screenshot(driver, 'login_failed.png')
                return False

        except Exception as e:
            print(f"Error during login: {str(e)}")
            self.take_screenshot(driver, 'login_error.png')
            return False
        
    def take_screenshot(self, driver, filename):
        """Save screenshot for debugging"""
        try:
            driver.save_screenshot(filename)
            print(f"Screenshot saved as {filename}")
        except Exception as e:
            print(f"Failed to take screenshot: {str(e)}")

    def test_login(self):
        """Test the login functionality"""
        try:
            print("Setting up Chrome driver with proxy...")
            driver = self.setup_driver()
            if not driver:
                raise Exception("Failed to initialize driver")

            print("Attempting to login...")
            login_success = self.login_to_x(driver)
            
            return {
                'success': login_success,
                'message': 'Login successful!' if login_success else 'Login failed',
                'proxy_server': self.proxy_server,
                'timestamp': datetime.now(timezone.utc).isoformat()
            }
                
        except Exception as e:
            print(f"Error in test_login: {str(e)}")
            self.cleanup_driver()  # Clean up on error
            return {
                'success': False,
                'error': str(e),
                'proxy_server': self.proxy_server,
                'timestamp': datetime.now(timezone.utc).isoformat()
            }