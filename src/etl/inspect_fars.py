import pandas as pd

DATA_DIR = "data/raw/fars_2024/FARS2024NationalCSV"

files = [
    "accident.csv",
    "vehicle.csv",
    "person.csv"
]

for file in files:
    path = f"{DATA_DIR}/{file}"
    df = pd.read_csv(path, encoding="latin1", low_memory=False)

    print(f"\n{file}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print(df.head(3))
    print()