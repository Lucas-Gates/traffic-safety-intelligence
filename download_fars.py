import os
import requests

URL = "https://static.nhtsa.gov/nhtsa/downloads/FARS/2024/National/FARS2024NationalCSV.zip"
OUTPUT_DIR = "data/raw"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "FARS2024NationalCSV.zip")


def download_fars():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    response = requests.get(URL, timeout=60)
    response.raise_for_status()
    with open(OUTPUT_FILE, "wb") as file:
        file.write(response.content)

    print(f"Downloaded FARS data to {OUTPUT_FILE}")


if __name__ == "__main__":
    download_fars()