import pandas as pd

DATA_DIR = "data/processed"

crashes = pd.read_csv(f"{DATA_DIR}/crashes.csv")
vehicles = pd.read_csv(f"{DATA_DIR}/vehicles.csv")
people = pd.read_csv(f"{DATA_DIR}/people.csv")

crash_keys = set(zip(crashes["STATE"], crashes["ST_CASE"]))
vehicle_keys = set(zip(vehicles["STATE"], vehicles["ST_CASE"], vehicles["VEH_NO"]))
people_with_vehicle = people[people["VEH_NO"] != 0]

person_vehicle_keys = set(
    zip(
        people_with_vehicle["STATE"],
        people_with_vehicle["ST_CASE"],
        people_with_vehicle["VEH_NO"]
    )
)

missing_vehicle_keys = person_vehicle_keys - vehicle_keys
missing_people = people[
    people.set_index(["STATE", "ST_CASE", "VEH_NO"]).index.isin(
        missing_vehicle_keys
    )
]

print("CRASH → VEHICLE RELATIONSHIP")
print(f"Missing crash records: {len(set(zip(vehicles['STATE'], vehicles['ST_CASE'])) - crash_keys)}")

print("\nPEOPLE WITHOUT MATCHING VEHICLE")
print(f"Records: {len(missing_people)}")

print("\nPERSON TYPES")
print(
    missing_people["PER_TYPNAME"]
    .value_counts()
    .head(20)
)

print("\nVEHICLE NUMBERS")
print(
    missing_people["VEH_NO"]
    .value_counts()
    .head(20)
)

print("\nSAMPLE RECORDS")
print(
    missing_people[
        ["STATE", "ST_CASE", "VEH_NO", "PER_NO", "PER_TYPNAME", "INJ_SEVNAME"]
    ].head(20)
)

print("\nPEDESTRIANS / NON-MOTORISTS")
print(f"VEH_NO = 0: {len(people[people['VEH_NO'] == 0])}")