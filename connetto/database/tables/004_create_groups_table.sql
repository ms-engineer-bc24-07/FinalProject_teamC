CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    company_id INT REFERENCES companies(id),
    meeting_date DATE NOT NULL,
    meeting_time TIME NOT NULL,
    leader_id INT REFERENCES users(id)
);
