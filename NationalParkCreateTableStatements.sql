CREATE DATABASE nationalParks;
USE nationalParks;

DROP TABLE IF EXISTS country;
DROP TABLE IF EXISTS state_province;
DROP TABLE IF EXISTS park;
DROP TABLE IF EXISTS lake;
DROP TABLE IF EXISTS mountain;
DROP TABLE IF EXISTS trail;

-- Country Table
CREATE TABLE country (
    id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL DEFAULT 'Missing Name',
    region VARCHAR(15) NOT NULL,
    CHECK(region IN ('Africa', 'Asia', 'Europe', 'Oceania', 'North America', 'South America'))
);

-- State_Province Table
CREATE TABLE state_province (
    id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL DEFAULT 'Missing State/Province',
    country_id INTEGER NOT NULL,
    FOREIGN KEY (country_id) REFERENCES country(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Park Table
CREATE TABLE park (
    id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL DEFAULT 'Missing National Park Name',
    visitors_per_year INTEGER,
    state_province_id INTEGER NOT NULL,
    area INTEGER,
    year_established INTEGER NOT NULL,
    FOREIGN KEY (state_province_id) REFERENCES state_province(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Lake Table
CREATE TABLE lake (
    id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL DEFAULT 'Missing Lake Name',
    park_id INTEGER NOT NULL,
    type VARCHAR(25),
    depth INTEGER,
    FOREIGN KEY (park_id) REFERENCES park(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Mountain Table
CREATE TABLE mountain (
    id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL DEFAULT 'Missing Mountain Name',
    park_id INTEGER NOT NULL,
    elevation INTEGER NOT NULL,
    FOREIGN KEY (park_id) REFERENCES park(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Trail Table
CREATE TABLE trail (
    id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL DEFAULT 'Missing Trail Name',
    park_id INTEGER NOT NULL,
    distance DECIMAL(6, 2),
    FOREIGN KEY (park_id) REFERENCES park(id) ON DELETE CASCADE ON UPDATE CASCADE
);