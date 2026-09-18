import os
import zipfile

YEARS = [2020, 2021, 2022, 2023, 2024]
RAW_DIR = "data/raw"

def extract_all():
    for year in YEARS:
        zip_path = os.path.join(RAW_DIR, f"FARS{year}NationalCSV.zip")
        out_dir = os.path.join(RAW_DIR, f"fars_{year}")
        if not os.path.exists(zip_path):
            continue
        os.makedirs(out_dir, exist_ok=True)
        print(f"Extracting {year}...")
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(out_dir)

if __name__ == "__main__":
    extract_all()