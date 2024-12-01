CREATE TABLE group_members (
    id SERIAL PRIMARY KEY,
    group_id INT REFERENCES groups(id),
    user_id INT REFERENCES users(id)
);
