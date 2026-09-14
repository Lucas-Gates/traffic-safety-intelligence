import os
import zipfile

ZIP_FILE = "data/raw/FARS2024NationalCSV.zip"
OUTPUT_DIR = "data/raw/fars_2024"

def extract_fars():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with zipfile.ZipFile(ZIP_FILE, "r") as zip_file:
        zip_file.extractall(OUTPUT_DIR)
    print(f"Extracted FARS data to {OUTPUT_DIR}")

if __name__ == "__main__":
    extract_fars()