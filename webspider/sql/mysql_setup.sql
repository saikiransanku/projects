CREATE DATABASE IF NOT EXISTS webmaster_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'webmaster_user'@'localhost'
  IDENTIFIED BY 'ChangeMe_StrongPassword123!';
GRANT ALL PRIVILEGES ON webmaster_db.* TO 'webmaster_user'@'localhost';

FLUSH PRIVILEGES;
