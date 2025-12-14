-- Fallback facts
CREATE TABLE IF NOT EXISTS fallback_facts (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    fact_text VARCHAR(255) NOT NULL,
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_enabled (enabled)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO fallback_facts (fact_text) VALUES
('A group of flamingos is called a flamboyance.'),
('Bananas are berries, but strawberries are not.'),
('Honey never spoils.'),
('Octopuses have three hearts.'),
('There are more stars in the universe than grains of sand on Earth.');

