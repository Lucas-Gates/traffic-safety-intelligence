import pandas as pd

DATA_DIR = "data/processed"

crashes = pd.read_csv(f"{DATA_DIR}/crashes.csv")
vehicles = pd.read_csv(f"{DATA_DIR}/vehicles.csv")
people = pd.read_csv(f"{DATA_DIR}/people.csv")

crash_keys = set(zip(crashes["STATE"], crashes["ST_CASE"]))
vehicle_keys = set(zip(vehicles["STATE"], vehicles["ST_CASE"]))
person_vehicle_keys = set(zip(people["STATE"], people["ST_CASE"], people["VEH_NO"]))

print("CRASH -> VEHICLE RELATIONSHIP")

vehicle_crash_keys = set(zip(vehicles["STATE"], vehicles["ST_CASE"]))

missing_vehicle_crashes = vehicle_crash_keys - crash_keys

print(f"Vehicle crash keys: {len(vehicle_crash_keys)}")
print(f"Missing crash records: {len(missing_vehicle_crashes)}")

print("\nVEHICLE -> PERSON RELATIONSHIP")

vehicle_person_keys = set(zip(vehicles["STATE"], vehicles["ST_CASE"], vehicles["VEH_NO"]))

person_keys_for_vehicles = set(
    zip(
        people.loc[people["VEH_NO"] != 0, "STATE"],
        people.loc[people["VEH_NO"] != 0, "ST_CASE"],
        people.loc[people["VEH_NO"] != 0, "VEH_NO"]
    )
)

missing_person_vehicles = person_keys_for_vehicles - vehicle_person_keys

print(f"Vehicle-person keys: {len(vehicle_person_keys)}")
print(f"Missing vehicle records: {len(missing_person_vehicles)}")

print("\nPEDESTRIANS / NON-MOTORISTS")

pedestrians = people[people["VEH_NO"] == 0]

print(f"People with VEH_NO = 0: {len(pedestrians)}")