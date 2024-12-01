CREATE TABLE venues (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    nearest_station VARCHAR(100),
    atmosphere VARCHAR(50)
);
