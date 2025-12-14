-- how to run: mysql -u root -p -e "SET @DB_PASSWORD := 'yourpass'; SOURCE conf/create_discord_bot_db.sql;"

-- Create database
CREATE DATABASE IF NOT EXISTS discord_bot
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- Expect @DB_PASSWORD to be set in the session before sourcing this file
-- Create user (safe if re-run)
CREATE USER IF NOT EXISTS 'discord_bot'@'localhost'
IDENTIFIED BY @DB_PASSWORD;

-- Grant privileges
GRANT ALL PRIVILEGES ON discord_bot.* TO 'discord_bot'@'localhost';

FLUSH PRIVILEGES;