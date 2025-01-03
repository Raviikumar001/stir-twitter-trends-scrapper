 def test_proxy_connection(self):
        """Test if ProxyMesh connection is working"""
        try:
            print("\n=== Testing ProxyMesh Connection ===")
            
            # Construct proxy URL with authentication
            proxy_url = f"http://{self.proxymesh_username}:{self.proxymesh_password}@{self.proxy_server}"
            proxies = {
                'http': proxy_url,
                'https': proxy_url
            }
            
            # Make a simple request to a basic website
            print(f"Testing proxy connection through: {self.proxy_server}")
            response = requests.get(
                'http://google.com',  # Simple test URL
                proxies=proxies,
                timeout=10
            )
            
            if response.status_code in [200, 301, 302]:
                print("✅ ProxyMesh connection successful!")
                return True
                
            print(f"❌ Connection failed with status: {response.status_code}")
            return False
            
        except requests.exceptions.ProxyError as e:
            print(f"❌ ProxyMesh Error: {str(e)}")
            return False
        except Exception as e:
            print(f"❌ Connection Error: {str(e)}")
            return False