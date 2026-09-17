-- schema.sql: Database schema for Traffic Safety Intelligence Platform
CREATE DATABASE IF NOT EXISTS traffic_safety;
USE traffic_safety;

DROP TABLE IF EXISTS people;
DROP TABLE IF EXISTS vehicles;
DROP TABLE IF EXISTS crashes;

-- 1. Crashes Table (Core Entity)
CREATE TABLE crashes (
    st_case INT PRIMARY KEY,
    state INT NOT NULL,
    statename VARCHAR(50),
    county INT,
    countyname VARCHAR(100),
    city INT,
    cityname VARCHAR(100),
    month INT,
    monthname VARCHAR(20),
    day INT,
    dayname VARCHAR(20),
    day_week INT,
    day_weekname VARCHAR(20),
    year INT NOT NULL,
    hour INT,
    minute INT,
    tway_id VARCHAR(100),
    route INT,
    rur_urb INT,
    rur_urbname VARCHAR(50),
    func_sys INT,
    func_sysname VARCHAR(100),
    latitude DECIMAL(10, 7),
    longitud DECIMAL(10, 7),
    harm_ev INT,
    harm_evname VARCHAR(100),
    man_coll INT,
    man_collname VARCHAR(100),
    reljct1 INT,
    reljct1name VARCHAR(100),
    reljct2 INT,
    reljct2name VARCHAR(100),
    typ_int INT,
    typ_intname VARCHAR(100),
    rel_road INT,
    rel_roadname VARCHAR(100),
    wrk_zone INT,
    wrk_zonename VARCHAR(100),
    lgt_cond INT,
    lgt_condname VARCHAR(100),
    weather INT,
    weathername VARCHAR(100),
    fatals INT NOT NULL DEFAULT 1,
    INDEX idx_crashes_state (state),
    INDEX idx_crashes_year (year)
);

-- 2. Vehicles Table
CREATE TABLE vehicles (
    st_case INT NOT NULL,
    veh_no INT NOT NULL,
    state INT NOT NULL,
    numoccs INT,
    hit_run INT,
    mod_year INT,
    makename VARCHAR(100),
    model INT,
    body_typname VARCHAR(100),
    rollover INT,
    trav_sp INT,
    speedrel INT,
    speedrelname VARCHAR(100),
    dr_drink INT,
    dr_drinkname VARCHAR(50),
    dr_pres INT,
    dr_presname VARCHAR(50),
    vtrafway INT,
    vtrafwayname VARCHAR(100),
    vnum_lan INT,
    vspd_lim INT,
    valign INT,
    vprofile INT,
    vpavetyp INT,
    vsurcond INT,
    vtrafcon INT,
    p_crash1 INT,
    p_crash1name VARCHAR(100),
    acc_type INT,
    acc_typename VARCHAR(150),
    deaths INT NOT NULL DEFAULT 0,
    PRIMARY KEY (st_case, veh_no),
    CONSTRAINT fk_vehicles_crashes FOREIGN KEY (st_case) 
        REFERENCES crashes (st_case) ON DELETE CASCADE
);

-- 3. People Table
-- Note: As discovered during validation, some non-motorists and non-transport occupants
-- are tracked without a matching vehicle row, so we reference crashes directly.
CREATE TABLE people (
    st_case INT NOT NULL,
    veh_no INT NOT NULL,
    per_no INT NOT NULL,
    state INT NOT NULL,
    age INT,
    sex INT,
    sexname VARCHAR(20),
    per_typ INT,
    per_typname VARCHAR(100),
    inj_sev INT,
    inj_sevname VARCHAR(100),
    seat_pos INT,
    seat_posname VARCHAR(100),
    rest_use INT,
    rest_usename VARCHAR(100),
    helm_use INT,
    helm_usename VARCHAR(100),
    air_bag INT,
    air_bagname VARCHAR(100),
    ejection INT,
    ejectionname VARCHAR(100),
    drinking INT,
    drinkingname VARCHAR(50),
    alc_status INT,
    alc_statusname VARCHAR(50),
    drugs INT,
    drugsname VARCHAR(50),
    hospital INT,
    hospitalname VARCHAR(100),
    doa INT,
    doaname VARCHAR(50),
    PRIMARY KEY (st_case, veh_no, per_no),
    CONSTRAINT fk_people_crashes FOREIGN KEY (st_case) 
        REFERENCES crashes (st_case) ON DELETE CASCADE
);