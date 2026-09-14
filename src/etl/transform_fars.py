import os
import pandas as pd

RAW_DIR = "data/raw/fars_2024/FARS2024NationalCSV"
PROCESSED_DIR = "data/processed"

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

def transform_file(filename, columns, output_name):
    input_path = os.path.join(RAW_DIR, filename)
    output_path = os.path.join(PROCESSED_DIR, output_name)
    df = pd.read_csv(input_path, encoding="latin1", low_memory=False)
    df = df[columns]
    df.to_csv(output_path, index=False)
    print(f"{output_name}: {len(df)} rows")

def main():
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    transform_file(
        "accident.csv",
        CRASH_COLUMNS,
        "crashes.csv"
    )

    transform_file(
        "vehicle.csv",
        VEHICLE_COLUMNS,
        "vehicles.csv"
    )

    transform_file(
        "person.csv",
        PERSON_COLUMNS,
        "people.csv"
    )

if __name__ == "__main__":
    main()