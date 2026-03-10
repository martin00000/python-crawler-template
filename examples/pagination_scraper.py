"""
Pagination Scraper Example - Crawl multiple pages.
分页爬虫示例 - 展示多页爬取功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import BaseScraper, get_random_user_agent


class PaginationScraper(BaseScraper):
    """Example scraper that handles paginated content."""
    
    def __init__(self, base_url: str, max_pages: int = 5):
        super().__init__(base_url, user_agent=get_random_user_agent())
        self.max_pages = max_pages
    
    def get_page_urls(self, page_num: int) -> str:
        """
        Generate URL for a specific page.
        Customize this based on the target site's URL structure.
        
        Examples:
            /page/2, /list?page=2, /item?offset=10&limit=10
        """
        # Modify based on your target site pattern
        if "?" in self.base_url:
            return f"{self.base_url}&page={page_num}"
        else:
            return f"{self.base_url}/page/{page_num}"
    
    def parse(self, response) -> list:
        """Extract data from current page."""
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(response.text, "lxml")
        items = []
        
        # Customize selector for your target site
        for item in soup.select(".item"):
            items.append({
                "title": item.select_one("h3")?.get_text(strip=True),
                "url": item.select_one("a")["href"] if item.select_one("a") else None,
                "description": item.select_one("p")?.get_text(strip=True)[:100],
            })
        
        return items
    
    def get_next_page_link(self, soup) -> str:
        """
        Find link to next page.
        Customize based on the target site's pagination UI.
        """
        # Common patterns:
        next_link = soup.select_one("a.next")
        if not next_link:
            next_link = soup.select_one('a[href*="page="]')
        
        if next_link and next_link.get("href"):
            from urllib.parse import urljoin
            return urljoin(self.base_url, next_link["href"])
        
        return None
    
    def crawl_all_pages(self):
        """Crawl all available pages until max_pages or no more pages."""
        all_items = []
        current_url = self.base_url
        page_count = 0
        
        print(f"Starting pagination crawl...")
        print(f"Max pages: {self.max_pages}\n")
        
        while current_url and page_count < self.max_pages:
            page_count += 1
            print(f"Crawling page {page_count}: {current_url}")
            
            try:
                response = self.fetch(current_url)
                items = self.parse(response)
                all_items.extend(items)
                
                print(f"  → Found {len(items)} items on this page")
                print(f"  → Total collected so far: {len(all_items)}\n")
                
                # Get next page
                soup = BeautifulSoup(response.text, "lxml")
                next_link = self.get_next_page_link(soup)
                
                if next_link and next_link != current_url:
                    current_url = next_link
                else:
                    print("No more pages found. Stopping.\n")
                    break
                    
            except Exception as e:
                print(f"  ✗ Error on page {page_count}: {e}\n")
                break
        
        return all_items


def main():
    """Run the pagination scraper example."""
    print("=" * 60)
    print("Pagination Scraper Example / 分页爬虫示例")
    print("=" * 60)
    
    # Target URL - Change to your desired target
    base_url = "https://example.com/list"
    max_pages = 5
    
    print(f"Base URL: {base_url}")
    print(f"Max pages to scrape: {max_pages}\n")
    
    try:
        scraper = PaginationScraper(base_url, max_pages=max_pages)
        all_data = scraper.crawl_all_pages()
        
        if all_data:
            # Save results
            output_file = "./output/paginated_results.csv"
            os.makedirs("./output", exist_ok=True)
            scraper.save(all_data, output_file)
            
            print("=" * 60)
            print(f"✓ Complete! Collected {len(all_data)} total items")
            print(f"  Saved to: {output_file}")
            print("=" * 60)
        else:
            print("No data was collected.")
            
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
