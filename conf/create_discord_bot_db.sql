-- how to run: mysql -u root -p < create_discord_bot_db.sql

-- Create database
CREATE DATABASE IF NOT EXISTS discord_bot
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- Create user (safe if re-run)
CREATE USER IF NOT EXISTS 'discord_bot'@'localhost'
IDENTIFIED BY 'STRONG_PASSWORD_HERE';

-- Grant privileges
GRANT ALL PRIVILEGES ON discord_bot.* TO 'discord_bot'@'localhost';

FLUSH PRIVILEGES;