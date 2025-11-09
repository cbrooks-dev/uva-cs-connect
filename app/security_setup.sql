
--Do NOT commit this file to a public repo.
--Run manually!


CREATE ROLE IF NOT EXISTS app_readonly;
CREATE ROLE IF NOT EXISTS app_user;
CREATE ROLE IF NOT EXISTS app_admin;

-- =========================================
-- 2. Grant Privileges to Roles
-- =========================================
-- Read-only: SELECT only
GRANT SELECT ON your_database_name.* TO app_readonly;

-- Regular app: can read/write but not alter schema
GRANT SELECT, INSERT, UPDATE, DELETE
ON your_database_name.* TO app_user;

-- Admin: can do almost everything
GRANT ALL PRIVILEGES ON your_database_name.* TO app_admin;
-- Note: Avoid WITH GRANT OPTION for app_admin unless absolutely needed

-- =========================================
-- 3. Create Application Users
-- =========================================
-- Replace ${...} placeholders during deployment with environment variables
CREATE USER IF NOT EXISTS 'app_readonly'@'%' IDENTIFIED BY '${APP_READONLY_PASS}';
CREATE USER IF NOT EXISTS 'app_user'@'%' IDENTIFIED BY '${APP_USER_PASS}';
CREATE USER IF NOT EXISTS 'app_admin'@'localhost' IDENTIFIED BY '${APP_ADMIN_PASS}';

-- =========================================
-- 4. Assign Roles to Users
-- =========================================
GRANT app_readonly TO 'app_readonly'@'%';
GRANT app_user TO 'app_user'@'%';
GRANT app_admin TO 'app_admin'@'localhost';

-- =========================================
-- 5. Enforce SSL Connections
-- =========================================
ALTER USER 'app_readonly'@'%' REQUIRE SSL;
ALTER USER 'app_user'@'%' REQUIRE SSL;
ALTER USER 'app_admin'@'localhost' REQUIRE SSL;

-- =========================================
-- 6. Password Hashing Trigger (Student Table)
-- =========================================
-- Hashes passwords automatically before insert/update using SHA2-256

DROP TRIGGER IF EXISTS hash_student_password;
DELIMITER $$
CREATE TRIGGER hash_student_password
BEFORE INSERT ON Student
FOR EACH ROW
BEGIN
  SET NEW.password = SHA2(NEW.password, 256);
END$$
DELIMITER ;

DROP TRIGGER IF EXISTS hash_student_password_update;
DELIMITER $$
CREATE TRIGGER hash_student_password_update
BEFORE UPDATE ON Student
FOR EACH ROW
BEGIN
  IF NEW.password <> OLD.password THEN
    SET NEW.password = SHA2(NEW.password, 256);
  END IF;
END$$
DELIMITER ;

-- =========================================
-- 7. Add Additional Data Integrity Checks
-- =========================================
-- Prevent invalid time ranges in AvailabilitySlot
ALTER TABLE AvailabilitySlot
ADD CONSTRAINT chk_time_valid CHECK (start_time < end_time);

-- =========================================
-- 8. Audit Logging (optional, if enabled)
-- =========================================
-- Enable general log for basic query tracking
-- (For production, use MySQL Enterprise Audit or Percona Audit Log)
SET GLOBAL general_log = 'ON';
SET GLOBAL log_output = 'FILE';
SET GLOBAL general_log_file = '/var/log/mysql/general.log';

-- =========================================
-- 9. Verify Roles & Grants
-- =========================================
SHOW GRANTS FOR 'app_readonly'@'%';
SHOW GRANTS FOR 'app_user'@'%';
SHOW GRANTS FOR 'app_admin'@'localhost';
