"""
Unit Tests for the crawler template.
爬虫模板单元测试
"""

import pytest
import os
import sys
from unittest.mock import Mock, patch

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils import (
    get_user_agents,
    get_random_user_agent,
    get_proxy,
    random_delay,
    generate_headers,
)


class TestUtils:
    """Test utility functions."""

    def test_get_user_agents_returns_list(self):
        """Test that get_user_agents returns a list."""
        agents = get_user_agents()
        assert isinstance(agents, list)
        assert len(agents) > 0

    def test_get_random_user_agent_valid(self):
        """Test that we get a valid user agent string."""
        ua = get_random_user_agent()
        assert isinstance(ua, str)
        assert len(ua) > 10
        assert "Mozilla" in ua or "Chrome" in ua

    @patch('src.utils.PROXY_POOL', ['http://test.com:8080'])
    def test_get_proxy_with_pool(self):
        """Test proxy retrieval from pool."""
        proxy = get_proxy()
        assert proxy == 'http://test.com:8080'

    def test_generate_headers_has_ua(self):
        """Test that generated headers include user agent."""
        headers = generate_headers()
        assert "User-Agent" in headers
        assert headers["User-Agent"] in get_user_agents()


class TestBaseScraper:
    """Test BaseScraper functionality (mocked)."""

    @pytest.fixture
    def mock_scraper(self):
        """Create a mock scraper instance."""
        from src.base import BaseScraper
        
        class TestScraper(BaseScraper):
            def parse(self, response):
                return []
        
        return TestScraper("https://example.com")

    def test_scraper_initialization(self, mock_scraper):
        """Test scraper initialization."""
        assert mock_scraper.base_url == "https://example.com"
        assert hasattr(mock_scraper, 'session')
        assert hasattr(mock_scraper, 'max_retries')

    @patch('requests.Session.get')
    def test_fetch_success(self, mock_get, mock_scraper):
        """Test successful fetch."""
        mock_response = Mock()
        mock_response.text = "<html></html>"
        mock_get.return_value = mock_response
        
        response = mock_scraper.fetch()
        assert response is mock_response
        mock_get.assert_called_once()


def test_file_structure():
    """Verify required files exist."""
    required_files = [
        "README.md",
        "setup.py",
        "requirements.txt",
        "config.yaml",
        "src/__init__.py",
        "src/base.py",
        "examples/simple_scraper.py",
    ]
    
    for file_path in required_files:
        full_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            file_path
        )
        assert os.path.exists(full_path), f"Missing required file: {file_path}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
