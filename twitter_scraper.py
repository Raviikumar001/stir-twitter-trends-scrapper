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
import uuid
import time
import atexit

class XScraper:
    def __init__(self):
        load_dotenv()
        self.mongodb_client = pymongo.MongoClient(os.getenv('MONGODB_URI'))
        self.db = self.mongodb_client['x_trends']
        self.collection = self.db['trends']
        
        # X credentials
        self.x_username = os.getenv('X_USERNAME')  # ravi-hisoka
        self.x_password = os.getenv('X_PASSWORD')
        
        print(f"\nCurrent Date and Time (UTC): {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Current User's Login: {self.x_username}")

        # Initialize the driver as a class attribute
        self.driver = None
        # Register cleanup function
        atexit.register(self.cleanup)

    def setup_driver(self):
        """Setup and return Chrome driver if not already initialized"""
        if self.driver is None:
            try:
                chrome_options = Options()
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--disable-dev-shm-usage')
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--disable-gpu')
                chrome_options.add_argument('--window-size=1920,1080')
                chrome_options.add_argument('--start-maximized')
                
                # Add anti-detection measures
                chrome_options.add_argument('--disable-blink-features=AutomationControlled')
                chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.109 Safari/537.36')
                chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
                chrome_options.add_experimental_option('useAutomationExtension', False)
                
                # Point to the Chrome binary installed in the Docker container
                chrome_options.binary_location = '/usr/local/bin/chrome'
                
                service = Service('/usr/local/bin/chromedriver')
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                
                # Mask WebDriver
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                
                return self.driver
            except Exception as e:
                print(f"Error in setup_driver: {str(e)}")
                raise

    def login_to_x(self):
        """Handle the X (Twitter) login process"""
        try:
            if self.driver is None:
                self.setup_driver()

            print(f"Starting login process at {datetime.now(timezone.utc)}")
            self.driver.get("https://x.com/login")
            time.sleep(3)  # Wait for page load

            # Enter username
            print("Locating username field...")
            username_field = self.driver.find_element(By.XPATH, "//input[@name='text']")
            print(f"Entering username: {self.x_username}")
            username_field.send_keys(self.x_username)
            
            # Click Next
            print("Clicking Next button...")
            next_button = self.driver.find_element(By.XPATH, "//span[contains(text(),'Next')]")
            next_button.click()
            time.sleep(3)  # Wait for password field

            # Enter password
            print("Entering password...")
            password_field = self.driver.find_element(By.XPATH, "//input[@name='password']")
            password_field.send_keys(self.x_password)
            
            # Click Login
            print("Clicking Login button...")
            login_button = self.driver.find_element(By.XPATH, "//span[contains(text(),'Log in')]")
            login_button.click()
            time.sleep(5)  # Wait for login to complete

            # Verify login success by checking for home feed
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Home')]"))
                )
                print("Successfully logged in")
                return True
            except Exception as e:
                print(f"Login verification failed: {str(e)}")
                self.take_screenshot('login_failed.png')
                return False

        except Exception as e:
            print(f"Error during login: {str(e)}")
            self.take_screenshot('login_error.png')
            return False

    def take_screenshot(self, filename):
        """Save screenshot for debugging"""
        try:
            if self.driver:
                self.driver.save_screenshot(filename)
                print(f"Screenshot saved as {filename}")
        except Exception as e:
            print(f"Failed to take screenshot: {str(e)}")

    def test_login(self):
        """Test the login functionality"""
        try:
            print("Setting up Chrome driver...")
            if self.driver is None:
                self.setup_driver()
            
            print("Attempting to login...")
            if self.login_to_x():
                print("Login test successful")
                return True
            else:
                print("Login test failed")
                return False
                
        except Exception as e:
            print(f"Error in test_login: {str(e)}")
            return False

    def cleanup(self):
        """Cleanup method to properly close the browser"""
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
                print("Browser closed successfully")
        except Exception as e:
            print(f"Error during cleanup: {str(e)}")

    def __del__(self):
        """Destructor to ensure cleanup"""
        self.cleanup()