"""
Scrapy Adapter - Integration with Scrapy framework.
Scrapy 适配器 - 与 Scrapy 框架集成
"""

import logging
from typing import Optional, Dict, Any, Iterator
from urllib.parse import urljoin
import scrapy
from scrapy.http import Response, Request

from .base import BaseScraper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ScrapyCrawler(BaseScraper):
    """
    Scrapy-based crawler extending BaseScraper functionality.
    基于 Scrapy 的爬虫扩展基础功能
    """

    def __init__(
        self,
        base_url: str,
        custom_settings: Optional[Dict] = None,
    ):
        """
        Initialize Scrapy crawler.
        
        Args:
            base_url: Starting URL for crawling
            custom_settings: Custom Scrapy settings
        """
        super().__init__(base_url)
        
        default_settings = {
            "ROBOTSTXT_OBEY": True,
            "CONCURRENT_REQUESTS": 32,
            "DOWNLOAD_DELAY": 1.0,
            "RANDOMIZE_DOWNLOAD_DELAY": True,
            "ITEM_PIPELINES": {
                "src.pipelines.DataValidationPipeline": 1,
            },
        }
        
        if custom_settings:
            default_settings.update(custom_settings)
            
        self.settings = default_settings

    def create_spider(
        self,
        name: str,
        parse_method,
        start_urls: Optional[list] = None,
        **kwargs
    ) -> type:
        """
        Dynamically create a Scrapy spider class.
        
        Args:
            name: Spider name
            parse_method: Parse function to handle responses
            start_urls: List of starting URLs
            **kwargs: Additional spider attributes
            
        Returns:
            Spider class ready to run
        """
        spider_class = type(
            name,
            (scrapy.Spider,),
            {
                "name": name,
                "start_urls": start_urls or [self.base_url],
                "custom_settings": self.settings,
                **kwargs,
            }
        )
        
        # Attach parse method dynamically
        spider_class.parse = parse_method
        
        return spider_class

    def run(self, spider_class: type, args: Optional[tuple] = None):
        """
        Run the spider using Scrapy.
        
        Args:
            spider_class: The spider class to run
            args: Arguments to pass to the spider
        """
        from scrapy.crawler import Crunner
        from twisted.internet import reactor
        
        # Create crawler instance
        crawler = self.create_crawler(spider_class)
        
        # Run the crawler
        Crunner(crawler).start()
        reactor.run()

    def create_crawler(self, spider_class: type) -> scrapy.crawler.Crawler:
        """Create and configure a crawler instance."""
        from scrapy.crawler import Crawler, CrawlerRunner
        from scrapy.utils.project import get_project_settings
        
        settings = get_project_settings()
        for key, value in self.settings.items():
            settings.set(key, value)
        
        runner = CrawlerRunner(settings)
        crawler = Crawler(spider_class, settings)
        return crawler


class ScrapyItem(scrapy.Item):
    """Base item class for Scrapy spiders."""
    
    # Define your fields here
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    timestamp = scrapy.Field()
