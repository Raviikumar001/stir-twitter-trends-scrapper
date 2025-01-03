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

class XScraper:
    def __init__(self):
        load_dotenv()
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
        
        print(f"\nCurrent Date and Time (UTC): {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Current User's Login: {self.x_username}")

    def setup_driver(self):
        try:
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--start-maximized')
            chrome_options.binary_location = '/usr/bin/google-chrome'
            
            # Add proxy configuration
            proxy_auth = f"{self.proxymesh_username}:{self.proxymesh_password}"
            chrome_options.add_argument(f'--proxy-server=http://{self.proxy_server}')
            
            # Add anti-detection measures
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument(f'--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')
            chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Initialize the driver with specific ChromeDriver path
            service = Service('/usr/local/bin/chromedriver')
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Add proxy authentication
            driver.execute_cdp_cmd('Network.enable', {})
            driver.execute_cdp_cmd('Network.setExtraHTTPHeaders', {
                'headers': {
                    'Proxy-Authorization': f'Basic {proxy_auth}'
                }
            })
            
            # Mask WebDriver
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            return driver
        except Exception as e:
            print(f"Error in setup_driver: {str(e)}")
            raise


    # Rest of your code remains exactly the same
    def login_to_x(self, driver):
        """Handle the X (Twitter) login process"""
        try:
            print(f"Starting login process at {datetime.now(timezone.utc)}")
            driver.get("https://x.com/login")
            time.sleep(3)  # Wait for page load

            # Enter username
            print("Locating username field...")
            username_field = driver.find_element(By.XPATH, "//input[@name='text']")
            print(f"Entering username: {self.x_username}")
            username_field.send_keys(self.x_username)
            
            # Click Next
            print("Clicking Next button...")
            next_button = driver.find_element(By.XPATH, "//span[contains(text(),'Next')]")
            next_button.click()
            time.sleep(3)  # Wait for password field

            # Enter password
            print("Entering password...")
            password_field = driver.find_element(By.XPATH, "//input[@name='password']")
            password_field.send_keys(self.x_password)
            
            # Click Login
            print("Clicking Login button...")
            login_button = driver.find_element(By.XPATH, "//span[contains(text(),'Log in')]")
            login_button.click()
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
        driver = None
        try:
            print("Setting up Chrome driver...")
            driver = self.setup_driver()
            
            print("Attempting to login...")
            if self.login_to_x(driver):
                print("Login test successful")
                return True
            else:
                print("Login test failed")
                return False
                
        except Exception as e:
            print(f"Error in test_login: {str(e)}")
            return False
        finally:
            if driver:
                driver.quit()



# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
# import pymongo
# from datetime import datetime, timezone
# import os
# from dotenv import load_dotenv
# import uuid
# import time

# class XScraper:
#     def __init__(self):
#         load_dotenv()
#         self.mongodb_client = pymongo.MongoClient(os.getenv('MONGODB_URI'))
#         self.db = self.mongodb_client['x_trends']
#         self.collection = self.db['trends']
        
#         # X credentials
#         self.x_username = os.getenv('X_USERNAME')
#         self.x_password = os.getenv('X_PASSWORD')

#     def setup_driver(self):
#         try:
#             chrome_options = Options()
#             chrome_options.add_argument('--no-sandbox')
#             chrome_options.add_argument('--disable-dev-shm-usage')
#             chrome_options.add_argument('--headless')
#             chrome_options.add_argument('--window-size=1920,1080')
#             chrome_options.add_argument('--start-maximized')
            
#             # Add anti-detection measures
#             chrome_options.add_argument('--disable-blink-features=AutomationControlled')
#             chrome_options.add_argument(f'--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
#             chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
#             chrome_options.add_experimental_option('useAutomationExtension', False)
            
#             # Initialize the driver
#             service = Service()
#             driver = webdriver.Chrome(service=service, options=chrome_options)
            
#             # Mask WebDriver
#             driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
#             return driver
#         except Exception as e:
#             print(f"Error in setup_driver: {str(e)}")
#             raise

#     def login_to_x(self, driver):
#         """Handle the X (Twitter) login process"""
#         try:
#             print(f"Starting login process at {datetime.now(timezone.utc)}")
#             driver.get("https://x.com/login")
#             time.sleep(3)  # Wait for page load

#             # Enter username
#             print("Locating username field...")
#             username_field = driver.find_element(By.XPATH, "//input[@name='text']")
#             print(f"Entering username: {self.x_username}")
#             username_field.send_keys(self.x_username)
            
#             # Click Next
#             print("Clicking Next button...")
#             next_button = driver.find_element(By.XPATH, "//span[contains(text(),'Next')]")
#             next_button.click()
#             time.sleep(3)  # Wait for password field

#             # Enter password
#             print("Entering password...")
#             password_field = driver.find_element(By.XPATH, "//input[@name='password']")
#             password_field.send_keys(self.x_password)
            
#             # Click Login
#             print("Clicking Login button...")
#             login_button = driver.find_element(By.XPATH, "//span[contains(text(),'Log in')]")
#             login_button.click()
#             time.sleep(5)  # Wait for login to complete

#             # Verify login success by checking for home feed
#             try:
#                 WebDriverWait(driver, 10).until(
#                     EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Home')]"))
#                 )
#                 print("Successfully logged in")
#                 return True
#             except Exception as e:
#                 print(f"Login verification failed: {str(e)}")
#                 self.take_screenshot(driver, 'login_failed.png')
#                 return False

#         except Exception as e:
#             print(f"Error during login: {str(e)}")
#             self.take_screenshot(driver, 'login_error.png')
#             return False

#     def take_screenshot(self, driver, filename):
#         """Save screenshot for debugging"""
#         try:
#             driver.save_screenshot(filename)
#             print(f"Screenshot saved as {filename}")
#         except Exception as e:
#             print(f"Failed to take screenshot: {str(e)}")

#     def test_login(self):
#         """Test the login functionality"""
#         driver = None
#         try:
#             print("Setting up Chrome driver...")
#             driver = self.setup_driver()
            
            
#             print("Attempting to login...")
#             if self.login_to_x(driver):
#                 print("Login test successful")
#                 return True
#             else:
#                 print("Login test failed")
#                 return False
                
#         except Exception as e:
#             print(f"Error in test_login: {str(e)}")
#             return False
#         finally:
#             if driver:
#                 driver.quit()