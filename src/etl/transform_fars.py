import glob
import os
import pandas as pd

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
YEARS = [2020, 2021, 2022, 2023, 2024]

CRASH_COLUMNS = [
    "STATE",
    "STATENAME",
    "ST_CASE",
    "COUNTY",
    "COUNTYNAME",
    "CITY",
    "CITYNAME",
    "MONTH",
    "MONTHNAME",
    "DAY",
    "DAYNAME",
    "DAY_WEEK",
    "DAY_WEEKNAME",
    "YEAR",
    "HOUR",
    "MINUTE",
    "TWAY_ID",
    "ROUTE",
    "RUR_URB",
    "RUR_URBNAME",
    "FUNC_SYS",
    "FUNC_SYSNAME",
    "LATITUDE",
    "LONGITUD",
    "HARM_EV",
    "HARM_EVNAME",
    "MAN_COLL",
    "MAN_COLLNAME",
    "RELJCT1",
    "RELJCT1NAME",
    "RELJCT2",
    "RELJCT2NAME",
    "TYP_INT",
    "TYP_INTNAME",
    "REL_ROAD",
    "REL_ROADNAME",
    "WRK_ZONE",
    "WRK_ZONENAME",
    "LGT_COND",
    "LGT_CONDNAME",
    "WEATHER",
    "WEATHERNAME",
    "FATALS"
]

VEHICLE_COLUMNS = [
    "STATE",
    "ST_CASE",
    "VEH_NO",
    "NUMOCCS",
    "HIT_RUN",
    "MOD_YEAR",
    "MAKENAME",
    "MODEL",
    "BODY_TYPNAME",
    "ROLLOVER",
    "TRAV_SP",
    "SPEEDREL",
    "SPEEDRELNAME",
    "DR_DRINK",
    "DR_DRINKNAME",
    "DR_PRES",
    "DR_PRESNAME",
    "VTRAFWAY",
    "VTRAFWAYNAME",
    "VNUM_LAN",
    "VSPD_LIM",
    "VALIGN",
    "VPROFILE",
    "VPAVETYP",
    "VSURCOND",
    "VTRAFCON",
    "P_CRASH1",
    "P_CRASH1NAME",
    "ACC_TYPE",
    "ACC_TYPENAME",
    "DEATHS"
]

PERSON_COLUMNS = [
    "STATE",
    "ST_CASE",
    "VEH_NO",
    "PER_NO",
    "AGE",
    "SEX",
    "SEXNAME",
    "PER_TYP",
    "PER_TYPNAME",
    "INJ_SEV",
    "INJ_SEVNAME",
    "SEAT_POS",
    "SEAT_POSNAME",
    "REST_USE",
    "REST_USENAME",
    "HELM_USE",
    "HELM_USENAME",
    "AIR_BAG",
    "AIR_BAGNAME",
    "EJECTION",
    "EJECTIONNAME",
    "DRINKING",
    "DRINKINGNAME",
    "ALC_STATUS",
    "ALC_STATUSNAME",
    "DRUGS",
    "DRUGSNAME",
    "HOSPITAL",
    "HOSPITALNAME",
    "DOA",
    "DOANAME"
]

def find_file(year, base_name):
    pattern = os.path.join(RAW_DIR, f"fars_{year}", "**", f"*{base_name}*")
    matches = glob.glob(pattern, recursive=True)
    for m in matches:
        if m.lower().endswith(f"{base_name.lower()}.csv"):
            return m
    return None

def process_entity(base_name, target_cols, output_name):
    dfs = []
    for yr in YEARS:
        file_path = find_file(yr, base_name)
        if file_path:
            df = pd.read_csv(file_path, encoding="latin1", low_memory=False)
            #reindex ensures all target columns exist even if one year missed a minor field
            df_filtered = df.reindex(columns=target_cols)
            dfs.append(df_filtered)
            print(f"  Loaded {yr} {base_name}: {len(df_filtered)} rows")
    merged = pd.concat(dfs, ignore_index=True)
    out_path = os.path.join(PROCESSED_DIR, output_name)
    merged.to_csv(out_path, index=False)
    print(f"Finished {output_name}: Total {len(merged)} rows\n")

def main():
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    print("Transforming Crashes...")
    process_entity("accident", CRASH_COLUMNS, "crashes.csv")
    print("Transforming Vehicles...")
    process_entity("vehicle", VEHICLE_COLUMNS, "vehicles.csv")
    print("Transforming People...")
    process_entity("person", PERSON_COLUMNS, "people.csv")

if __name__ == "__main__":
    main()