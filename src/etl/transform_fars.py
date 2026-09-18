import glob
import os
import pandas as pd

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
YEARS = [2020, 2021, 2022, 2023, 2024]

CRASH_COLUMNS = [
    "YEAR",
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
    "YEAR",
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
    "YEAR",
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

def find_file(year, exact_name):
    pattern = os.path.join(RAW_DIR, f"fars_{year}", "**", "*.csv")
    for file_path in glob.glob(pattern, recursive=True):
        base = os.path.basename(file_path).lower()
        if base == f"{exact_name.lower()}.csv":
            return file_path
    return None

def process_entity(target_filename, target_cols, output_name, dedupe_keys):
    dfs = []
    for yr in YEARS:
        file_path = find_file(yr, target_filename)
        if file_path:
            df = pd.read_csv(file_path, encoding="latin1", low_memory=False)
            df.columns = [c.strip().upper() for c in df.columns]
            if "YEAR" not in df.columns:
                df["YEAR"] = yr
            else:
                df["YEAR"] = df["YEAR"].fillna(yr).astype(int)
            if "STATE" not in df.columns and "STATE_CODE" in df.columns:
                df["STATE"] = df["STATE_CODE"]
            if "STATE" not in df.columns and "ST_CASE" in df.columns:
                df["STATE"] = df["ST_CASE"].astype(str).str.zfill(6).str[:2].astype(int)
            selected_data = {}
            for col in target_cols:
                if col in df.columns:
                    selected_data[col] = df[col]
                else:
                    selected_data[col] = None
            df_filtered = pd.DataFrame(selected_data)
            dfs.append(df_filtered)
            print(f"  Loaded {yr} {target_filename}: {len(df_filtered)} rows")
    merged = pd.concat(dfs, ignore_index=True)
    initial_count = len(merged)
    merged = merged.drop_duplicates(subset=dedupe_keys)
    dropped = initial_count - len(merged)
    if dropped > 0:
        print(f"  Dropped {dropped} duplicate rows for {output_name}")
    out_path = os.path.join(PROCESSED_DIR, output_name)
    merged.to_csv(out_path, index=False)
    print(f"Finished {output_name}: Total {len(merged)} rows\n")

def main():
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    print("Transforming Crashes...")
    process_entity("accident", CRASH_COLUMNS, "crashes.csv", ["YEAR", "ST_CASE"])
    print("Transforming Vehicles...")
    process_entity("vehicle", VEHICLE_COLUMNS, "vehicles.csv", ["YEAR", "ST_CASE", "VEH_NO"])
    print("Transforming People...")
    process_entity("person", PERSON_COLUMNS, "people.csv", ["YEAR", "ST_CASE", "VEH_NO", "PER_NO"])

if __name__ == "__main__":
    main()