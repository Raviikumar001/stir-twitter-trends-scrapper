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
        self.mongodb_client = pymongo.MongoClient(os.getenv('MONGODB_URI'))
        self.db = self.mongodb_client['x_trends']
        self.collection = self.db['trends']
        
        # X credentials
        self.x_username = os.getenv('X_USERNAME')  # ravi-hisoka
        self.x_password = os.getenv('X_PASSWORD')
        
        # ProxyMesh Configuration
        self.proxymesh_username = os.getenv('PROXYMESH_USERNAME')
        self.proxymesh_password = os.getenv('PROXYMESH_PASSWORD')
        self.proxy_server = 'us-ca.proxymesh.com:31280'
        
        # Current time tracking
        self.current_time_utc = datetime.now(timezone.utc)
        print(f"Current Date and Time (UTC): {self.current_time_utc.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Current User's Login: {self.x_username}\n")

    def get_proxy_url(self):
        """Get proxy URL with authentication"""
        return f"http://{self.proxymesh_username}:{self.proxymesh_password}@{self.proxy_server}"

    def test_proxy_connection(self):
        """Test if proxy connection is working"""
        try:
            print(f"\nTesting proxy connection at {self.current_time_utc.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Using proxy server: {self.proxy_server}")
            
            proxy_url = self.get_proxy_url()
            proxies = {
                'http': proxy_url,
                'https': proxy_url
            }
            
            # Test the proxy with a simple request to X
            print("Testing proxy connection to X...")
            response = requests.get(
                'https://twitter.com',
                proxies=proxies,
                timeout=10
            )
            
            if response.status_code in [200, 301, 302]:
                print("✅ Proxy connection successful!")
                return True
            
            print(f"❌ Connection failed with status code: {response.status_code}")
            return False
            
        except requests.exceptions.ProxyError as e:
            print(f"❌ Proxy Error: {str(e)}")
            return False
        except Exception as e:
            print(f"❌ Unexpected Error: {str(e)}")
            return False

    def setup_driver(self):
        """Set up Chrome driver with ProxyMesh"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--window-size=1920,1080')
            
            # Configure proxy
            proxy_with_auth = f"{self.proxymesh_username}:{self.proxymesh_password}@{self.proxy_server}"
            chrome_options.add_argument(f'--proxy-server=http://{self.proxy_server}')
            chrome_options.add_argument(f'--proxy-auth={self.proxymesh_username}:{self.proxymesh_password}')
            
            # Anti-detection measures
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument(f'--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            service = Service()
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            print(f"\nSelenium: Using proxy server {self.proxy_server}")
            return driver
            
        except Exception as e:
            print(f"❌ Error in setup_driver: {str(e)}")
            raise

    def verify_proxy_with_selenium(self, driver):
        """Verify proxy is working with Selenium"""
        try:
            print("\nVerifying Selenium proxy configuration...")
            # Test connection to X
            driver.get('https://twitter.com')
            time.sleep(3)
            
            # Check if we can access the page
            if "twitter.com" in driver.current_url.lower():
                print("✅ Selenium proxy verification successful!")
                return True
            
            print("❌ Failed to access X through proxy")
            return False
            
        except Exception as e:
            print(f"❌ Selenium proxy verification failed: {str(e)}")
            return False

    def test_full_proxy_setup(self):
        """Test both requests and selenium proxy setup"""
        try:
            print("\n=== Starting Proxy Test ===")
            print(f"DateTime (UTC): {self.current_time_utc.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"User: {self.x_username}")
            print(f"Proxy Server: {self.proxy_server}")
            
            # Test with requests
            requests_success = self.test_proxy_connection()
            
            # Test with Selenium
            driver = None
            try:
                driver = self.setup_driver()
                selenium_success = self.verify_proxy_with_selenium(driver)
            finally:
                if driver:
                    driver.quit()
            
            result = {
                'success': requests_success and selenium_success,
                'requests_test': requests_success,
                'selenium_test': selenium_success,
                'proxy_server': self.proxy_server,
                'username': self.x_username,
                'timestamp': self.current_time_utc.isoformat()
            }
            
            print("\n=== Test Results ===")
            print(f"Requests Test: {'✅ Passed' if requests_success else '❌ Failed'}")
            print(f"Selenium Test: {'✅ Passed' if selenium_success else '❌ Failed'}")
            
            return result
            
        except Exception as e:
            print(f"❌ Full proxy test failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'username': self.x_username,
                'proxy_server': self.proxy_server,
                'timestamp': self.current_time_utc.isoformat()
            }
        

    
   