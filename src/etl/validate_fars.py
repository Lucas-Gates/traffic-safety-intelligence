import pandas as pd

DATA_DIR = "data/processed"

crashes = pd.read_csv(f"{DATA_DIR}/crashes.csv")
vehicles = pd.read_csv(f"{DATA_DIR}/vehicles.csv")
people = pd.read_csv(f"{DATA_DIR}/people.csv")

print("DATASET SIZES")
print(f"Crashes: {len(crashes)}")
print(f"Vehicles: {len(vehicles)}")
print(f"People: {len(people)}")

print("\nCRASH KEYS")
print(f"Unique ST_CASE values: {crashes['ST_CASE'].nunique()}")
print(f"Duplicate ST_CASE values: {crashes['ST_CASE'].duplicated().sum()}")

print("\nVEHICLE KEYS")
vehicle_keys = vehicles[["STATE", "ST_CASE", "VEH_NO"]]
print(f"Duplicate vehicle keys: {vehicle_keys.duplicated().sum()}")

print("\nPERSON KEYS")
person_keys = people[["STATE", "ST_CASE", "VEH_NO", "PER_NO"]]
print(f"Duplicate person keys: {person_keys.duplicated().sum()}")

print("\nMISSING VALUES")
print("\nCrashes:")
print(crashes.isna().sum().sort_values(ascending=False).head(10))

print("\nVehicles:")
print(vehicles.isna().sum().sort_values(ascending=False).head(10))

print("\nPeople:")
print(people.isna().sum().sort_values(ascending=False).head(10))