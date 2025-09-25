#DefiLlama
import requests
import pandas as pd
from datetime import datetime

API_URL = "https://api.llama.fi/raises"

def fetch_defillama_raises():
    r = requests.get(API_URL, timeout=15)
    r.raise_for_status()
    data = r.json()

    # ✅ Extract only the raises list
    raises = data.get("raises", [])
    if not raises:
        print("⚠️ No fundraising data found.")
        return pd.DataFrame()

    # ✅ Convert to DataFrame
    df = pd.DataFrame(raises)

    # ✅ Convert Unix timestamp to human-readable date
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], unit="s")

    # ✅ Flatten nested list fields into comma-separated strings
    if "leadInvestors" in df.columns:
        df["leadInvestors"] = df["leadInvestors"].apply(lambda x: ", ".join(x) if isinstance(x, list) else "")
    if "otherInvestors" in df.columns:
        df["otherInvestors"] = df["otherInvestors"].apply(lambda x: ", ".join(x) if isinstance(x, list) else "")
    if "chains" in df.columns:
        df["chains"] = df["chains"].apply(lambda x: ", ".join(x) if isinstance(x, list) else "")

    # ✅ Sort by date (newest first)
    if "date" in df.columns:
        df = df.sort_values(by="date", ascending=False).reset_index(drop=True)

    print(f"✅ Found {len(df)} fundraising events from DefiLlama (sorted by date)")
    return df

if __name__ == "__main__":
    df = fetch_defillama_raises()

    if not df.empty:
        # Save to CSV
        csv_filename = "DefiLlama_Fundraising.csv"
        df.to_csv(csv_filename, index=False)
        print(f"💾 Data saved to {csv_filename}")

        # Show first 5 rows
        print("\n📊 Preview of data:")
        print(df.head())
    else:
        print("📁 No data to save.")
