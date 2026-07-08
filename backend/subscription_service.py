import httpx
from typing import Dict, Optional
from datetime import datetime

# GitHub raw URLs
SUBSCRIPTIONS_URL = "https://raw.githubusercontent.com/rohcuan/rohtembak/main/cli/subscriptions.txt"
PASSWORDS_URL = "https://raw.githubusercontent.com/rohcuan/rohtembak/main/cli/pass.txt"

class SubscriptionService:
    def __init__(self):
        self.subscriptions: Dict[str, str] = {}  # username -> expiry
        self.passwords: Dict[str, str] = {}  # username -> password
        self.last_fetch: Optional[datetime] = None
    
    async def fetch_subscriptions(self):
        """Fetch subscription data from GitHub"""
        async with httpx.AsyncClient() as client:
            try:
                # Fetch subscriptions
                sub_response = await client.get(SUBSCRIPTIONS_URL)
                sub_response.raise_for_status()
                
                # Fetch passwords
                pass_response = await client.get(PASSWORDS_URL)
                pass_response.raise_for_status()
                
                # Parse subscriptions (format: username / expiry)
                self.subscriptions = {}
                for line in sub_response.text.strip().split('\n'):
                    line = line.strip()
                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue
                    if ' / ' in line:
                        username, expiry = line.split(' / ', 1)
                        self.subscriptions[username.strip()] = expiry.strip()
                
                # Parse passwords (format: username / password)
                self.passwords = {}
                for line in pass_response.text.strip().split('\n'):
                    line = line.strip()
                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue
                    if ' / ' in line:
                        username, password = line.split(' / ', 1)
                        self.passwords[username.strip()] = password.strip()
                
                self.last_fetch = datetime.now()
                return True
            except Exception as e:
                print(f"Error fetching subscriptions: {e}")
                return False
    
    async def authenticate(self, username: str, password: str) -> Optional[Dict]:
        """Authenticate user with subscription"""
        # Fetch if not loaded or older than 5 minutes
        if self.last_fetch is None or (datetime.now() - self.last_fetch).seconds > 300:
            await self.fetch_subscriptions()
        
        # Check if user exists
        if username not in self.subscriptions:
            return None
        
        # Check password
        if username not in self.passwords or self.passwords[username] != password:
            return None
        
        # Return subscription data
        return {
            "username": username,
            "subscription_expiry": self.subscriptions[username]
        }

# Global instance
subscription_service = SubscriptionService()
