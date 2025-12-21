-- Command prefixes
CREATE TABLE IF NOT EXISTS command_prefixes (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    command VARCHAR(64) NOT NULL UNIQUE,
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    description VARCHAR(255) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO command_prefixes (command) VALUES
('$play'),
('$cmds'),
('$pause'),
('$resume'),
('$stop'),
('$queue'),
('$commands'),
('$key_words'),
('$weather'),
('$weather5'),
('$weather15'),
('$ChatMode'),
('$kysmetche');

