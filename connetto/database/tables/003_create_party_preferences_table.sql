CREATE TABLE party_preferences (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    date DATE NOT NULL,
    time TIME NOT NULL,
    gender_preference VARCHAR(20),
    age_preference VARCHAR(20),
    join_year_preference VARCHAR(20),
    department_preference VARCHAR(50),
    venue_preference VARCHAR(50)
);
