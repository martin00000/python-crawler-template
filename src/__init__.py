"""
Python Crawler Template - A production-ready web scraping framework.
爬虫工具包 - 生产级网络爬取框架
"""

from .base import BaseScraper
from .utils import get_user_agents, get_proxy, random_delay

__version__ = "1.0.0"
__all__ = [
    "BaseScraper",
    "get_user_agents",
    "get_proxy",
    "random_delay",
]
