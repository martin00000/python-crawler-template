"""
Utility functions for web scraping.
爬虫工具函数 - 代理、UA 池、延时等
"""

import time
import random
from typing import List, Optional


# User Agent Pool / UA 池
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
]


def get_user_agents() -> List[str]:
    """Get list of all user agents."""
    return USER_AGENTS.copy()


def get_random_user_agent() -> str:
    """Get a random user agent from the pool."""
    return random.choice(USER_AGENTS)


# Proxy IP Pool (Sample - replace with your actual proxy providers)
PROXY_POOL = [
    "http://proxy1.example.com:8080",
    "http://proxy2.example.com:8080",
    "http://proxy3.example.com:8080",
]


def get_proxy(proxy_list: Optional[List[str]] = None) -> Optional[str]:
    """
    Get a random proxy from the pool.
    
    Args:
        proxy_list: Custom proxy list (uses default pool if not provided)
        
    Returns:
        Proxy URL or None if no proxies available
    """
    pool = proxy_list or PROXY_POOL
    return random.choice(pool) if pool else None


# Random Delay
def random_delay(min_seconds: float = 1.0, max_seconds: float = 3.0) -> None:
    """
    Sleep for a random duration between min and max seconds.
    
    Args:
        min_seconds: Minimum delay in seconds
        max_seconds: Maximum delay in seconds
    """
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)


# Headers Generator
def generate_headers(custom_headers: Optional[Dict] = None) -> Dict:
    """
    Generate request headers with randomized user agent.
    
    Args:
        custom_headers: Additional custom headers
        
    Returns:
        Complete headers dictionary
    """
    base_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
        "User-Agent": get_random_user_agent(),
    }
    
    if custom_headers:
        base_headers.update(custom_headers)
    
    return base_headers


# Retry Logic Helper
def exponential_backoff(attempt: int, base_delay: float = 1.0, max_delay: float = 60.0) -> float:
    """
    Calculate delay for exponential backoff retry strategy.
    
    Args:
        attempt: Current retry attempt number (0-indexed)
        base_delay: Base delay in seconds
        max_delay: Maximum delay cap in seconds
        
    Returns:
        Delay duration in seconds
    """
    delay = min(base_delay * (2 ** attempt), max_delay)
    return delay
