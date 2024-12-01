CREATE VIEW preference_view AS
SELECT u.name, p.date, p.time, p.gender_restriction, p.age_restriction
FROM preferences p
JOIN users u ON p.user_id = u.id;
