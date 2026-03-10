"""
Login Scraper Example - Handling authentication.
登录验证爬虫示例 - 展示带认证的爬取功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import BaseScraper, get_random_user_agent
import requests


class LoginScraper(BaseScraper):
    """Example scraper that handles login and authenticated content."""
    
    def __init__(
        self,
        base_url: str,
        login_url: str,
        username: str,
        password: str,
        **kwargs
    ):
        """
        Initialize the login-enabled scraper.
        
        Args:
            base_url: Target URL after login
            login_url: Login page URL
            username: Username for authentication
            password: Password for authentication
        """
        super().__init__(base_url, **kwargs)
        
        self.login_url = login_url
        self.username = username
        self.password = password
        
        # Use session to persist cookies across requests
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": get_random_user_agent()})
    
    def login(self) -> bool:
        """
        Perform login and save session cookies.
        
        Returns:
            True if login successful, False otherwise
        """
        print(f"Logging in to {self.login_url}...")
        
        # Prepare login form data (customize field names!)
        login_data = {
            "username": self.username,
            "password": self.password,
            # Add other fields as needed:
            # "csrf_token": self._get_csrf_token(),
        }
        
        try:
            response = self.session.post(
                self.login_url,
                data=login_data,
                allow_redirects=True,
                timeout=30
            )
            
            # Check if login was successful
            if "logout" in response.text.lower() or "dashboard" in response.url.lower():
                print("✓ Login successful!")
                return True
            else:
                print("✗ Login failed - check credentials or form structure")
                return False
                
        except Exception as e:
            print(f"✗ Login error: {e}")
            return False
    
    def fetch_authenticated(self, url: str) -> requests.Response:
        """
        Fetch a page with preserved session cookies (after login).
        
        Args:
            url: Target URL
            
        Returns:
            HTTP response object
        """
        response = self.session.get(url, timeout=30)
        
        # Check if session expired
        if "login" in response.url and url != self.login_url:
            print("Session expired! Attempting re-login...")
            if not self.login():
                raise Exception("Re-login failed")
            response = self.session.get(url, timeout=30)
        
        return response
    
    def parse(self, response) -> list:
        """Parse authenticated content."""
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(response.text, "lxml")
        items = []
        
        # Customize parser for your target
        for item in soup.select(".protected-content"):
            items.append({
                "title": item.select_one("h2")?.get_text(strip=True),
                "data": item.select_one(".info")?.get_text(strip=True),
            })
        
        return items


def main():
    """Run the login scraper example."""
    print("=" * 60)
    print("Login Scraper Example / 登录验证爬虫示例")
    print("=" * 60)
    
    # Configuration - CHANGE THESE!
    config = {
        "base_url": "https://example.com/protected-area",
        "login_url": "https://example.com/login",
        "username": "your_username_here",  # TODO: Replace with real credentials
        "password": "your_password_here",  # TODO: Replace with real credentials
    }
    
    print(f"\nConfiguration:")
    for key, value in config.items():
        print(f"  {key}: {value}")
    
    print("\n⚠️  Note: This example requires valid credentials.")
    print("   Please update config with your actual login details.\n")
    
    try:
        # Create scraper instance
        scraper = LoginScraper(**config)
        
        # Perform login
        if not scraper.login():
            print("\nStopping due to login failure.")
            return
        
        # Fetch protected content
        print(f"\nCrawling protected content at {config['base_url']}...")
        response = scraper.fetch_authenticated(config["base_url"])
        
        # Parse and process
        data = scraper.parse(response)
        print(f"\nFound {len(data)} protected items")
        
        # Save results
        output_file = "./output/protected_data.csv"
        os.makedirs("./output", exist_ok=True)
        scraper.save(data, output_file)
        print(f"✓ Saved to {output_file}")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
