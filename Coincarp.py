# CoinCarp Multi-Page Scraper
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

def fetch_coincarp_fundraising(pages=3):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    all_data = []

    try:
        for page in range(1, pages+1):
            url = "https://www.coincarp.com/fundraising/" if page == 1 else f"https://www.coincarp.com/fundraising/?page={page}"
            print(f"🔍 Loading CoinCarp fundraising data from page {page}...")

            driver.get(url)

            # Wait until table is present
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "fundraisingListTable"))
            )
            time.sleep(2)  # give some extra time for JS to populate data

            table = driver.find_element(By.ID, "fundraisingListTable")
            rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # skip header row
            
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) >= 6:
                    all_data.append({
                        "Project": cells[0].text.strip(),
                        "Category": cells[1].text.strip(),
                        "Funding Round": cells[2].text.strip(),
                        "Amount": cells[3].text.strip(),
                        "Investors": cells[4].text.strip(),
                        "Funding Date": cells[5].text.strip()
                    })

            print(f"✅ Page {page}: collected {len(rows)} records.")
            time.sleep(1)

        if not all_data:
            print("⚠️ No data found on any page")
            return

        df = pd.DataFrame(all_data)
        csv_filename = "CoinCarp_Fundraising.csv"
        df.to_csv(csv_filename, index=False)
        print(f"✅ Saved {len(df)} total fundraising records to '{csv_filename}'")
        print("\n📊 First 5 entries:")
        print(df.head())

    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    fetch_coincarp_fundraising(pages=3)
