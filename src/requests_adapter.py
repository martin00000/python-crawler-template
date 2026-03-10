"""
Requests Adapter - Simple HTTP-based crawler.
Requests 适配器 - 简单的基于 HTTP 的爬取器
"""

import logging
from typing import Optional, Dict, Any, List
import requests
from bs4 import BeautifulSoup
import pandas as pd

from .base import BaseScraper
from .utils import get_random_user_agent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RequestsCrawler(BaseScraper):
    """
    Simple crawler using only requests and BeautifulSoup.
    仅使用 requests 和 BeautifulSoup 的简单爬虫
    """

    def __init__(
        self,
        base_url: str,
        use_soup: bool = True,
        **kwargs
    ):
        """
        Initialize the requests-based crawler.
        
        Args:
            base_url: Target URL
            use_soup: Whether to use BeautifulSoup for HTML parsing
            **kwargs: Additional arguments passed to BaseScraper
        """
        super().__init__(base_url, **kwargs)
        self.use_soup = use_soup

    def fetch_html(self, url: Optional[str] = None) -> str:
        """
        Fetch and return raw HTML content.
        
        Args:
            url: Target URL
            
        Returns:
            Raw HTML string
        """
        response = self.fetch(url)
        return response.text

    def parse_html(self, html: str) -> BeautifulSoup:
        """
        Parse HTML with BeautifulSoup.
        
        Args:
            html: Raw HTML string
            
        Returns:
            BeautifulSoup object
        """
        return BeautifulSoup(html, "lxml")

    def extract_links(self, soup: BeautifulSoup, absolute: bool = True) -> List[str]:
        """
        Extract all links from HTML.
        
        Args:
            soup: Parsed BeautifulSoup object
            absolute: Return absolute URLs if True
            
        Returns:
            List of URLs
        """
        links = []
        for link in soup.find_all("a", href=True):
            href = link["href"]
            if absolute:
                href = urljoin(self.base_url, href)
            links.append(href)
        return links

    def scrape_page(self, url: Optional[str] = None) -> Dict[str, Any]:
        """
        Scrape a single page and extract structured data.
        
        Args:
            url: Target URL
            
        Returns:
            Dictionary with extracted data
        """
        html = self.fetch_html(url)
        soup = self.parse_html(html)
        
        result = {
            "url": url or self.base_url,
            "title": soup.title.string if soup.title else None,
            "links": self.extract_links(soup),
            "text": soup.get_text(separator=" ", strip=True)[:1000],
        }
        
        return result


def urljoin(base: str, relative: str) -> str:
    """Join base and relative URLs."""
    from urllib.parse import urljoin as _urljoin
    return _urljoin(base, relative)


# Example Parser Classes / 示例解析器类

class ArticleParser:
    """Parse article pages."""
    
    @staticmethod
    def parse(soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract article metadata."""
        return {
            "title": soup.select_one("h1")?.get_text(strip=True) or soup.title?.string,
            "author": soup.select_one("meta[name='author']")?.get("content"),
            "published": soup.select_one("meta[property='article:published_time']")?.get("content"),
            "content": "\n".join(p.get_text(strip=True) for p in soup.select("p")),
        }


class ProductParser:
    """Parse product listings."""
    
    @staticmethod
    def parse_product(product_div) -> Dict[str, Any]:
        """Extract single product info."""
        return {
            "name": product_div.select_one(".product-name")?.get_text(strip=True),
            "price": product_div.select_one(".price")?.get_text(strip=True),
            "link": product_div.find("a")?.get("href") if product_div.find("a") else None,
        }
