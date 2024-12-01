CREATE TRIGGER log_user_action
AFTER INSERT ON users
FOR EACH ROW
EXECUTE FUNCTION log_user_action_function();
