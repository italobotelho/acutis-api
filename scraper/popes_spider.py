import requests
from bs4 import BeautifulSoup
import json
import os
import time

class GCatholicPopesSpider:
    """
    Spider responsible for extracting the papal lineage from GCatholic.org
    and saving it in JSON format (Seed Data).
    """
    
    def __init__(self):
        # Bot disguise and standard headers
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        # Official URL for the chronological list
        self.url = "http://www.gcatholic.org/hierarchy/pope/lineage.htm"

    def fetch_and_save(self):
        print(f"[*] Accessing {self.url}...")
        
        try:
            # GOOD PRACTICE: 2-second pause to avoid overloading their server
            time.sleep(2) 
            
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            popes_data = self._parse_table(soup)
            
            if popes_data:
                self._save_to_json(popes_data)
            
        except requests.exceptions.RequestException as e:
            print(f"[!] Connection error with GCatholic: {e}")

    def _parse_table(self, soup):
        popes_list = []
        
        # Find all tables on the page
        tables = soup.find_all('table')
        if not tables:
            print("[!] No tables found in the HTML.")
            return []
            
        # Senior Tactic: The main table is usually the one with the most rows (<tr>)
        main_table = max(tables, key=lambda t: len(t.find_all('tr')))
        rows = main_table.find_all('tr')
        
        print(f"[*] Main table found with {len(rows)} rows. Processing...")
        
        # Iterate row by row, ignoring the header
        for row in rows:
            cols = row.find_all('td')
            
            # If the row has enough data (avoids empty or divider rows)
            if len(cols) >= 4: 
                try:
                    # Clean up using list comprehension and strip
                    clean_cols = [" ".join(col.text.split()) for col in cols]
                    
                    pope = {
                        "succession_number": clean_cols[0],
                        "papal_name": clean_cols[1],
                        "pontificate_start": clean_cols[2],
                        "pontificate_end": clean_cols[3],
                        "notes": clean_cols[4] if len(clean_cols) > 4 else None
                    }
                    
                    # Ensure we only capture rows where the first column is a valid number (e.g., "266")
                    if pope["succession_number"].isdigit():
                        popes_list.append(pope)
                        
                except Exception as e:
                    # Ignore failures on broken rows and continue
                    continue
                    
        return popes_list

    def _save_to_json(self, data):
        """
        Ensures the /data folder exists and saves the JSON file.
        """
        # Creates the 'data' folder in the project root if it doesn't exist
        os.makedirs('data', exist_ok=True)
        filepath = 'data/popes.json'
        
        # Saves the file preserving special characters
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            
        print(f"\n=== SUCCESS: {len(data)} Popes extracted and structured ===")
        print(f"[*] Data safely saved to: {filepath}")

# ==========================================
# Execution Block
# ==========================================
if __name__ == "__main__":
    spider = GCatholicPopesSpider()
    spider.fetch_and_save()