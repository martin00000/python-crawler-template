"""
Base Scraper Class - Core functionality for web scraping.
基础爬虫类 - 网络爬取核心功能
"""

import time
import random
import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
import requests
from bs4 import BeautifulSoup

from .utils import get_user_agents, random_delay

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """
    Abstract base class for all scrapers.
    所有爬虫的抽象基类
    """

    def __init__(
        self,
        base_url: str,
        user_agent: Optional[str] = None,
        proxy: Optional[str] = None,
        delay_range: tuple = (1, 3),
        max_retries: int = 3,
    ):
        """
        Initialize the scraper with default settings.
        
        Args:
            base_url: Base URL to scrape
            user_agent: Custom user agent string
            proxy: Proxy server URL
            delay_range: Tuple of (min, max) delay in seconds
            max_retries: Maximum retry attempts
        """
        self.base_url = base_url
        self.user_agent = user_agent or random.choice(get_user_agents())
        self.proxy = proxy
        self.delay_range = delay_range
        self.max_retries = max_retries
        
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.user_agent})
        
        if proxy:
            self.session.proxies.update({
                "http": proxy,
                "https": proxy,
            })

    @abstractmethod
    def parse(self, response: requests.Response) -> List[Dict[str, Any]]:
        """
        Parse the response and extract data.
        
        Args:
            response: HTTP response object
            
        Returns:
            List of extracted data items
        """
        pass

    def fetch(self, url: Optional[str] = None) -> requests.Response:
        """
        Fetch a webpage with retry logic.
        
        Args:
            url: Target URL (uses base_url if not provided)
            
        Returns:
            HTTP response object
        """
        target_url = url or self.base_url
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Fetching {target_url} (attempt {attempt + 1})")
                response = self.session.get(target_url, timeout=30)
                response.raise_for_status()
                
                random_delay(*self.delay_range)
                return response
                
            except requests.RequestException as e:
                last_error = e
                logger.warning(f"Failed to fetch: {e}")
                time.sleep(2 ** attempt)  # Exponential backoff
        
        raise Exception(f"Failed to fetch after {self.max_retries} attempts: {last_error}")

    def save(self, data: List[Dict[str, Any]], filename: str, format: str = "csv"):
        """
        Save scraped data to file.
        
        Args:
            data: List of data dictionaries
            filename: Output filename
            format: Output format (csv, json, xlsx)
        """
        import pandas as pd
        
        df = pd.DataFrame(data)
        
        if format == "csv":
            df.to_csv(filename, index=False, encoding="utf-8-sig")
        elif format == "json":
            df.to_json(filename, orient="records", force_ascii=False, indent=2)
        elif format == "xlsx":
            df.to_excel(filename, index=False)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        logger.info(f"Saved {len(data)} records to {filename}")
