---
metadata:
  name: "web-scraper"
  version: "1.0.0"
  description: "Build a robust web scraper with rate limiting, error handling, and data export"
  category: "automation"
  tags: ["scraping", "automation", "python", "beautifulsoup", "requests"]
  author: "skillhub"
  created: "2024-01-15"
  updated: "2024-01-15"

requirements:
  os: ["linux", "macos", "windows"]
  python: ">=3.9"
  packages:
    - requests>=2.28.0
    - beautifulsoup4>=4.11.0
    - lxml>=4.9.0
    - pandas>=2.0.0
    - selenium>=4.0.0
  hardware:
    - ram: ">=2GB"
    - disk_space: ">=1GB"

estimated_time: "25-35 minutes"
difficulty: "intermediate"
---

# Web Scraper Setup

## Overview
This skill builds a production-ready web scraper with proper rate limiting, error handling, retry logic, and multiple export formats. Includes both static (BeautifulSoup) and dynamic (Selenium) scraping capabilities.

## Task Description
Complete web scraper implementation:
1. Set up Python environment with required libraries
2. Build base scraper with rate limiting and retries
3. Implement HTML parsing with BeautifulSoup
4. Add Selenium for JavaScript-heavy sites
5. Create data storage and export utilities
6. Add logging and monitoring
7. Implement respect for robots.txt

## Prerequisites
- Python 3.9+ installed
- Basic HTML/CSS understanding
- Target website to scrape (we'll use example sites)
- Chrome/Firefox browser (for Selenium)

## Steps

### 1. Environment Setup
```bash
# Create project directory
mkdir web_scraper
cd web_scraper

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install requests beautifulsoup4 lxml pandas selenium

# For Selenium, install webdriver
pip install webdriver-manager
```

### 2. Create Project Structure
```bash
# Create directories
mkdir -p {data,logs,scrapers}

# Create config file
cat > config.py << 'EOF'
import os

# Scraping configuration
USER_AGENT = 'Mozilla/5.0 (compatible; MyBot/1.0)'
REQUEST_TIMEOUT = 30
RATE_LIMIT_DELAY = 1  # seconds between requests
MAX_RETRIES = 3

# Output configuration
DATA_DIR = 'data'
LOGS_DIR = 'logs'

# Create directories
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)
EOF
```

### 3. Base Scraper Class
```python
# scrapers/base_scraper.py
import requests
import time
import logging
from typing import Optional
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

class BaseScraper:
    def __init__(self, base_url: str, rate_limit: float = 1.0):
        self.base_url = base_url
        self.rate_limit = rate_limit
        self.last_request_time = 0
        self.session = self._create_session()

    def _create_session(self):
        """Create session with retry logic."""
        session = requests.Session()

        # Configure retries
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        # Set headers
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; MyBot/1.0)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        })

        return session

    def _rate_limit_wait(self):
        """Enforce rate limiting between requests."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit:
            time.sleep(self.rate_limit - elapsed)
        self.last_request_time = time.time()

    def fetch_page(self, url: str) -> Optional[str]:
        """Fetch a page with rate limiting and error handling."""
        self._rate_limit_wait()

        try:
            logger.info(f"Fetching: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            logger.info(f"Successfully fetched: {url} (Status: {response.status_code})")
            return response.text

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return None

    def parse_html(self, html: str) -> BeautifulSoup:
        """Parse HTML with BeautifulSoup."""
        return BeautifulSoup(html, 'lxml')

    def get_absolute_url(self, url: str) -> str:
        """Convert relative URL to absolute."""
        return urljoin(self.base_url, url)

# Example usage
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    scraper = BaseScraper('https://example.com')
    html = scraper.fetch_page('https://example.com')

    if html:
        soup = scraper.parse_html(html)
        print(f"Title: {soup.title.string if soup.title else 'No title'}")
```

### 4. Product Scraper Example
```python
# scrapers/product_scraper.py
import pandas as pd
from base_scraper import BaseScraper
import logging

logger = logging.getLogger(__name__)

class ProductScraper(BaseScraper):
    def __init__(self, base_url: str):
        super().__init__(base_url, rate_limit=2.0)
        self.products = []

    def scrape_product_list(self, url: str):
        """Scrape product listing page."""
        html = self.fetch_page(url)
        if not html:
            return

        soup = self.parse_html(html)

        # Example: Scraping product cards
        # Adjust selectors based on target website structure
        product_cards = soup.find_all('div', class_='product-card')

        logger.info(f"Found {len(product_cards)} products")

        for card in product_cards:
            product = self._extract_product_data(card)
            if product:
                self.products.append(product)

    def _extract_product_data(self, card) -> dict:
        """Extract product data from HTML element."""
        try:
            # Adjust selectors for your target website
            name = card.find('h2', class_='product-name')
            price = card.find('span', class_='price')
            link = card.find('a', class_='product-link')

            product = {
                'name': name.text.strip() if name else 'N/A',
                'price': price.text.strip() if price else 'N/A',
                'url': self.get_absolute_url(link['href']) if link else 'N/A',
            }

            logger.debug(f"Extracted: {product['name']}")
            return product

        except Exception as e:
            logger.error(f"Failed to extract product: {e}")
            return None

    def save_to_csv(self, filename: str):
        """Save scraped data to CSV."""
        if not self.products:
            logger.warning("No products to save")
            return

        df = pd.DataFrame(self.products)
        df.to_csv(filename, index=False)
        logger.info(f"Saved {len(self.products)} products to {filename}")

    def save_to_json(self, filename: str):
        """Save scraped data to JSON."""
        if not self.products:
            logger.warning("No products to save")
            return

        df = pd.DataFrame(self.products)
        df.to_json(filename, orient='records', indent=2)
        logger.info(f"Saved {len(self.products)} products to {filename}")

# Example usage
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    # Example with a demo site (replace with actual target)
    scraper = ProductScraper('https://books.toscrape.com')
    scraper.scrape_product_list('https://books.toscrape.com/catalogue/page-1.html')

    # Save results
    scraper.save_to_csv('data/products.csv')
    scraper.save_to_json('data/products.json')

    print(f"\nScraped {len(scraper.products)} products")
```

### 5. Dynamic Scraper with Selenium
```python
# scrapers/dynamic_scraper.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import logging
import time

logger = logging.getLogger(__name__)

class DynamicScraper:
    def __init__(self, headless: bool = True):
        self.driver = self._setup_driver(headless)

    def _setup_driver(self, headless: bool):
        """Set up Chrome WebDriver."""
        options = webdriver.ChromeOptions()

        if headless:
            options.add_argument('--headless')

        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        return driver

    def fetch_page(self, url: str, wait_time: int = 10):
        """Fetch page and wait for JavaScript to load."""
        logger.info(f"Loading: {url}")
        self.driver.get(url)

        # Wait for page to load
        time.sleep(2)

        return self.driver.page_source

    def wait_for_element(self, selector: str, by: By = By.CSS_SELECTOR, timeout: int = 10):
        """Wait for element to be present."""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, selector))
            )
            return element
        except Exception as e:
            logger.error(f"Element not found: {selector} - {e}")
            return None

    def scroll_to_bottom(self, pause_time: float = 1.0):
        """Scroll to bottom of page (for infinite scroll)."""
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(pause_time)

            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def close(self):
        """Close the browser."""
        self.driver.quit()

# Example usage
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    scraper = DynamicScraper(headless=True)

    try:
        # Example: Scrape a JavaScript-heavy site
        scraper.fetch_page('https://example.com')

        # Wait for specific element
        element = scraper.wait_for_element('h1')
        if element:
            print(f"Found: {element.text}")

        # Get page source after JS execution
        html = scraper.driver.page_source
        print(f"HTML length: {len(html)} characters")

    finally:
        scraper.close()
```

### 6. Main Scraper Script
```python
# main.py
import logging
from datetime import datetime
from scrapers.product_scraper import ProductScraper
import sys

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/scraper_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Main scraping workflow."""
    logger.info("=" * 60)
    logger.info("Starting Web Scraper")
    logger.info("=" * 60)

    try:
        # Initialize scraper
        # Example using books.toscrape.com (a safe practice site)
        scraper = ProductScraper('https://books.toscrape.com')

        # Scrape multiple pages
        for page in range(1, 4):  # Scrape first 3 pages
            url = f'https://books.toscrape.com/catalogue/page-{page}.html'
            logger.info(f"Scraping page {page}...")
            scraper.scrape_product_list(url)

        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        scraper.save_to_csv(f'data/products_{timestamp}.csv')
        scraper.save_to_json(f'data/products_{timestamp}.json')

        # Summary
        logger.info("=" * 60)
        logger.info(f"Scraping completed successfully!")
        logger.info(f"Total products scraped: {len(scraper.products)}")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"Scraping failed: {e}", exc_info=True)
        raise

if __name__ == '__main__':
    main()
```

### 7. Run the Scraper
```bash
# Run the scraper
python main.py

# View results
ls -lh data/
head data/products_*.csv
```

## Expected Output
- `data/products_YYYYMMDD_HHMMSS.csv`: Scraped data in CSV format
- `data/products_YYYYMMDD_HHMMSS.json`: Scraped data in JSON format
- `logs/scraper_YYYYMMDD_HHMMSS.log`: Detailed execution log
- Console output with progress and summary

## Troubleshooting

### Rate Limiting / 429 Errors
```python
# Increase delay between requests
scraper = BaseScraper(base_url, rate_limit=5.0)  # 5 seconds
```

### Selenium ChromeDriver Issues
```bash
# Update ChromeDriver
pip install --upgrade webdriver-manager

# Use Firefox instead
pip install geckodriver-autoinstaller
```

### Parsing Errors
```python
# Debug HTML structure
soup = scraper.parse_html(html)
print(soup.prettify()[:1000])  # Print first 1000 chars
```

### Connection Timeouts
```python
# Increase timeout
response = self.session.get(url, timeout=60)  # 60 seconds
```

## Success Criteria
- [x] Scraper runs without crashing
- [x] Data extracted from multiple pages
- [x] Rate limiting enforced (no 429 errors)
- [x] Data saved to CSV and JSON formats
- [x] Log file created with execution details
- [x] No data loss or corruption
- [x] Handles errors gracefully

## Next Steps
- Add proxy support for IP rotation
- Implement concurrent scraping with threading
- Add data validation and cleaning
- Set up scheduled scraping with cron
- Store data in database instead of files
- Add email notifications for failures
- Implement captcha solving (with caution)
- Add data deduplication

## Related Skills
- `api-scraping`
- `data-cleaning`
- `schedule-tasks`
- `proxy-rotation`

## References
- [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests Documentation](https://docs.python-requests.org/)
- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [Web Scraping Best Practices](https://scrapinghub.com/guides/web-scraping-best-practices)
- [Robots.txt Guidelines](https://developers.google.com/search/docs/crawling-indexing/robots/intro)
