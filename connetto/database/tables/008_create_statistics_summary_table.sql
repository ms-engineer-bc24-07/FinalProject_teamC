CREATE TABLE statistics_summary (
    id SERIAL PRIMARY KEY,
    department VARCHAR(50),
    month INT,
    year INT,
    total_parties INT,
    total_participants INT
);
