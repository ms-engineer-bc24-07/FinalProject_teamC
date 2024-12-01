CREATE VIEW meetup_view AS
SELECT u.name, m.meetup_date, m.meetup_time, m.gender_restriction, m.age_restriction
FROM meetups m
JOIN users u ON m.user_id = u.id;
