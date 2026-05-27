import requests
from bs4 import BeautifulSoup
import json
import os
import time
import re
from urllib.parse import urljoin

class GCatholicDeepSpider:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'http://www.gcatholic.org/'
        }
        self.start_url = "http://www.gcatholic.org/hierarchy/pope/"

    def fetch_and_save(self):
        print(f"[*] Accessing main lineage page: {self.start_url}...")
        response = requests.get(self.start_url, headers=self.headers, timeout=15)
        
        print(f"[*] Server Response Code: {response.status_code}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        tables = soup.find_all('table')
        
        if not tables:
            print("[!] FATAL: No tables found on the page.")
            print("[?] HTML snapshot (First 500 chars):")
            print(response.text[:500])
            return 
            
        main_table = max(tables, key=lambda t: len(t.find_all('tr')))
        rows = main_table.find_all('tr')
        
        popes_list = []
        
        print(f"[*] Starting Deep Crawl for {len(rows)} potential records. This may take 3-5 minutes...")
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 4:
                num_text = cols[0].text.strip()
                
                if num_text.isdigit():
                    pope_data = {
                        "succession_number": num_text,
                        "papal_name": " ".join(cols[1].text.split()),
                        "pontificate_start": " ".join(cols[2].text.split()),
                        "pontificate_end": " ".join(cols[3].text.split()),
                        "notes": " ".join(cols[4].text.split()) if len(cols) > 4 else None
                    }
                    
                    a_tag = cols[1].find('a')
                    if a_tag and 'href' in a_tag.attrs:
                        profile_url = urljoin(self.start_url, a_tag['href'])
                        
                        enriched_data = self._scrape_profile(profile_url)
                        pope_data.update(enriched_data)
                        
                        # Politeness delay to avoid server blocks
                        time.sleep(1)
                        
                    popes_list.append(pope_data)
                    
        self._save_to_json(popes_list)

    def _scrape_profile(self, url):
        print(f"    [>] Deep Scraping profile: {url}")
        
        data = {
            "baptism_name": None, "profile_pontificate_start": None, "profile_pontificate_end": None,
            "birth_date": None, "birth_place": None, "episcopal_motto": None, 
            "cardinals_created": 0, "documents_issued": 0, "saints_proclaimed": 0, "blesseds_proclaimed": 0,
            "ordained_priest_date": None, "consecrated_bishop_date": None,
            "created_cardinal_date": None, "elected_pontiff_date": None,
            "installed_pontiff_date": None, "death_date": None, "death_place": None,
            "beatified_date": None, "canonised_date": None, "feast_day": None,
            "buried_at": None, "religious_order": None
        }
        
        try:
            resp = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            lines = [line.strip() for line in soup.get_text(separator='\n').splitlines() if line.strip()]
            
            # 1. Parse Header (Name and basic dates)
            for i in range(min(10, len(lines))):
                line = lines[i]
                
                if line.startswith('(') and line.endswith(')') and re.match(r'^\([A-Za-z\s\.\,\-]+\)$', line):
                    data["baptism_name"] = line.strip('()').strip()
                    
                if re.match(r'^\d{1,4}[\d\.\?]*\s*[-–]', line):
                    parts = re.split(r'[-–]', line)
                    if len(parts) >= 2:
                        data["profile_pontificate_start"] = parts[0].strip()
                        data["profile_pontificate_end"] = parts[1].strip()

            # 2. Extract Religious Order
            for line in lines:
                if line.startswith("Priest of ") and any(x in line for x in ["Order", "Society", "Congregation", "Friars", "Monks"]):
                    m = re.search(r'Priest of (.*?)\s*\(\d{4}', line)
                    if m:
                        data["religious_order"] = m.group(1).strip()
                        break
                        
            text = ' '.join(lines)
            
            def extract(pattern):
                match = re.search(pattern, text, re.IGNORECASE)
                return match.group(1).strip() if match else None

            # 3. Extract Complex Dates (Birth and Death)
            born_match = re.search(r'Born:\s*(?:([\d\.\?]+)\s*)?\((.*?)\)', text)
            if born_match:
                if born_match.group(1): data["birth_date"] = born_match.group(1).replace('.', '-')
                data["birth_place"] = born_match.group(2).strip()
                
            died_match = re.search(r'Died:\s*([\d\.\?]+)\s*🩸?\s*\((.*?)(?:†|outlived|\))', text)
            if died_match:
                data["death_date"] = died_match.group(1).replace('.', '-')
                data["death_place"] = died_match.group(2).strip().strip('(').strip()

            # 4. Extract Standard Metrics
            data["episcopal_motto"] = extract(r'Episcopal Motto:\s*([^B]+)Born:')
            data["ordained_priest_date"] = extract(r'Ordained Priest:\s*([\d\.\?]+)')
            data["consecrated_bishop_date"] = extract(r'Consecrated Bishop:\s*([\d\.\?]+)')
            data["created_cardinal_date"] = extract(r'Created Cardinal:\s*([\d\.\?]+)')
            data["elected_pontiff_date"] = extract(r'Elected as Supreme Pontiff:\s*([\d\.\?]+)')
            data["installed_pontiff_date"] = extract(r'Installed as Supreme Pontiff:\s*([\d\.\?]+)')
            data["beatified_date"] = extract(r'Beatified:\s*([\d\.\?]+)')
            data["canonised_date"] = extract(r'Canonised:\s*([\d\.\?]+)')
            
            feast = extract(r'Feast:\s*([\d\.\-]+)')
            if feast: 
                data["feast_day"] = feast.replace('.', '-')

            # 5. Statistics
            if card := extract(r'(\d+)\s*Cardinals'): data["cardinals_created"] = int(card)
            if doc := extract(r'(\d+)\s*Documents'): data["documents_issued"] = int(doc)
            if saint := extract(r'(\d+)\s*Saints'): data["saints_proclaimed"] = int(saint)
            if bless := extract(r'(\d+)\s*Blesseds'): data["blesseds_proclaimed"] = int(bless)

            # 6. Burial Place (Cleaning navigation artifacts)
            burial_match = re.search(r'Buried at:\s*(.*?)(?:©|$)', text)
            if burial_match:
                b_text = burial_match.group(1).strip()
                b_text = re.sub(r'\s*Pope\s+[A-Z].*$', '', b_text)
                data["buried_at"] = b_text.strip()
                
        except Exception as e:
            print(f"    [!] Failed to deep scrape: {e}")
            
        return data

    def _save_to_json(self, data):
        os.makedirs('data', exist_ok=True)
        with open('data/popes.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"\n=== SUCCESS: {len(data)} Enriched Popes saved! ===")

if __name__ == "__main__":
    spider = GCatholicDeepSpider()
    spider.fetch_and_save()