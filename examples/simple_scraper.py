"""
Simple Scraper Example - Basic usage of the crawler template.
简单爬虫示例 - 展示基础用法
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import BaseScraper, get_random_user_agent


class SimpleArticleScraper(BaseScraper):
    """Example scraper that extracts article titles and links."""
    
    def __init__(self, base_url: str):
        super().__init__(base_url, user_agent=get_random_user_agent())
    
    def parse(self, response) -> list:
        """Extract article information from HTML."""
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(response.text, "lxml")
        articles = []
        
        # Find all article elements (customize selector for your target site)
        for article in soup.select("article"):
            title_elem = article.select_one("h2 a")
            link_elem = article.select_one("a")
            
            if title_elem and link_elem:
                articles.append({
                    "title": title_elem.get_text(strip=True),
                    "url": link_elem["href"],
                    "summary": article.select_one("p")?.get_text(strip=True)[:200] if article.select_one("p") else None,
                })
        
        return articles


def main():
    """Run the example scraper."""
    print("=" * 60)
    print("Simple Scraper Example / 简单爬虫示例")
    print("=" * 60)
    
    # Target URL - Change this to your desired scraping target
    target_url = "https://example.com"
    
    print(f"\nTarget URL: {target_url}")
    print("Scraping in progress...\n")
    
    try:
        # Create scraper instance
        scraper = SimpleArticleScraper(target_url)
        
        # Fetch and parse
        response = scraper.fetch()
        data = scraper.parse(response)
        
        # Display results
        print(f"\nFound {len(data)} articles:")
        print("-" * 60)
        
        for i, item in enumerate(data[:5], 1):  # Show first 5 items
            print(f"{i}. {item['title']}")
            print(f"   URL: {item['url']}")
            if item['summary']:
                print(f"   Summary: {item['summary']}...")
            print()
        
        # Save to CSV
        output_file = "./output/articles.csv"
        os.makedirs("./output", exist_ok=True)
        scraper.save(data, output_file)
        print(f"\n✓ Saved {len(data)} records to {output_file}")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
