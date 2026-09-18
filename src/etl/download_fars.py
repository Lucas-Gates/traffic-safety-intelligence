import os
import requests

YEARS = [2020, 2021, 2022, 2023, 2024]
OUTPUT_DIR = "data/raw"

def download_fars_years():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for year in YEARS:
        url = f"https://static.nhtsa.gov/nhtsa/downloads/FARS/{year}/National/FARS{year}NationalCSV.zip"
        dest = os.path.join(OUTPUT_DIR, f"FARS{year}NationalCSV.zip")
        if os.path.exists(dest):
            print(f"Skipping {year}, already downloaded.")
            continue
        print(f"Downloading FARS {year}...")
        res = requests.get(url, timeout=120)
        res.raise_for_status()
        with open(dest, "wb") as f:
            f.write(res.content)
        print(f"Saved {dest}")

if __name__ == "__main__":
    download_fars_years()