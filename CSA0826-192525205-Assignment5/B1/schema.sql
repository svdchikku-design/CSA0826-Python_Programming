-- Design from Task A1.2
CREATE TABLE stations (
    station_id  INTEGER PRIMARY KEY,
    name        TEXT NOT NULL UNIQUE,
    temp_unit   TEXT NOT NULL CHECK (temp_unit IN ('C', 'F'))      -- unit used in the RAW file; stored data are always Celsius
);
CREATE TABLE readings (
    station_id  INTEGER NOT NULL REFERENCES stations(station_id),
    date        TEXT    NOT NULL,                                   -- 'YYYY-MM-DD'
    hour        INTEGER NOT NULL CHECK (hour BETWEEN 0 AND 23),
    pm25        REAL,                                               -- NULL = missing (never 0 as a stand-in)
    pm10        REAL,
    no2         REAL,
    temp_c      REAL,
    PRIMARY KEY (station_id, date, hour)                            -- one reading per station per hour: rejects duplicates
) WITHOUT ROWID;
