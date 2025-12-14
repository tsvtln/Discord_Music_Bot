-- Config table
CREATE TABLE IF NOT EXISTS config (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    config_key VARCHAR(100) NOT NULL UNIQUE,
    config_value TEXT NOT NULL,
    description VARCHAR(255) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO config (config_key, config_value, description) VALUES
('SSHUSR', '', 'SSH username'),
('S2', '', 'SSH target server'),
('WEATHER_API_KEY', '', 'Weather API key'),
('BOT_KEY', '', 'Discord bot token'),
('timeout', '', 'GIF timeout in seconds');

