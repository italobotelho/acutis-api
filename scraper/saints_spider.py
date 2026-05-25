import requests
from bs4 import BeautifulSoup
import json

class WikipediaSaintSpider:
    """
    A web scraper designed to extract Saint biographies from Wikipedia.
    """
    
    def __init__(self):
        # We use headers to simulate a real browser, preventing blocks
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.base_url = "https://en.wikipedia.org/wiki/"

    def fetch_saint_data(self, saint_url_slug):
        """
        Fetches and parses the HTML of a given saint.
        Example slug: 'Carlo_Acutis'
        """
        url = f"{self.base_url}{saint_url_slug}"
        print(f"[*] Crawling: {url}")
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status() # Raises an error for bad responses (404, 500)
            
            # Parse the HTML with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract data
            saint_data = self._extract_information(soup)
            return saint_data
            
        except requests.exceptions.RequestException as e:
            print(f"[!] Error fetching data for {saint_url_slug}: {e}")
            return None

    def _extract_information(self, soup):
        """
        Internal method to parse specific HTML tags and build our dictionary.
        """
        data = {}
        
        # 1. Get the Official Name (H1 tag)
        title_tag = soup.find('h1', id='firstHeading')
        data['official_name'] = title_tag.text.strip() if title_tag else None
        
        # 2. Ultra-resilient paragraph extraction
        # 'mw-content-text' is the safest ID for Wikipedia main content globally
        content_div = soup.find('div', id='mw-content-text')
        
        if content_div:
            # Find all paragraph tags anywhere inside the content area
            paragraphs = content_div.find_all('p')
            
            valid_paragraphs = []
            for p in paragraphs:
                # get_text() extracts all text, ignoring internal HTML tags (like <a> or <b>)
                text = p.get_text(separator=' ', strip=True)
                
                # Filter out very short paragraphs (like empty lines or coordinate captions)
                if len(text) > 50:
                    valid_paragraphs.append(text)
            
            # --- DEBUG LINE: Let's see what the spider is actually seeing ---
            print(f"[*] Debug: Found {len(valid_paragraphs)} valid paragraphs.")
            
            if valid_paragraphs:
                data['short_bio'] = valid_paragraphs[0]
                data['full_bio'] = "\n\n".join(valid_paragraphs[:5])
            else:
                data['short_bio'] = None
                data['full_bio'] = None
        else:
            print("[!] Debug: Could not find 'mw-content-text' div.")
            data['short_bio'] = None
            data['full_bio'] = None
            
        # 3. Default manual assignments for our first test
        data['current_status'] = "Blessed" 
        data['gender'] = "M"
        
        return data

# ==========================================
# Execution Block (For local testing)
# ==========================================
if __name__ == "__main__":
    spider = WikipediaSaintSpider()
    
    # Let's test with our project's inspiration!
    acutis_data = spider.fetch_saint_data("Carlo_Acutis")
    
    if acutis_data:
        print("\n=== SUCCESS: DATA EXTRACTED ===")
        # Print the dictionary formatted as JSON
        print(json.dumps(acutis_data, indent=4, ensure_ascii=False))