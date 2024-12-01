ALTER TABLE meetups ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id);
ALTER TABLE preferences ADD CONSTRAINT fk_user_pref FOREIGN KEY (user_id) REFERENCES users(id);
