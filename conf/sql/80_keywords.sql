-- Keyword groups and keywords
CREATE TABLE IF NOT EXISTS keyword_groups (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    group_name VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(255),
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS keywords (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    keyword VARCHAR(50) NOT NULL,
    group_id INT UNSIGNED NOT NULL,
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_keywords_group FOREIGN KEY (group_id) REFERENCES keyword_groups(id) ON DELETE CASCADE,
    UNIQUE KEY uniq_keyword_group (keyword, group_id),
    INDEX idx_keyword (keyword)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO keyword_groups (group_name, description) VALUES
('beer', 'Beer related keywords'),
('kur', 'Kur jokes'),
('usl', 'Useless / Angel / A4o'),
('bot', 'Bot keywords'),
('haralampi', 'Haralampi keywords'),
('wednesday', 'Wednesday memes'),
('d1', 'Day 1 keywords'),
('booba', 'Booba / boobs keywords');

INSERT INTO keywords (keyword, group_id)
SELECT k, g.id FROM keyword_groups g,
(SELECT 'бири' k UNION ALL SELECT 'бира' UNION ALL SELECT 'bira' UNION ALL SELECT 'biri' UNION ALL SELECT 'beer') x
WHERE g.group_name = 'beer';

INSERT INTO keywords (keyword, group_id)
SELECT k, g.id FROM keyword_groups g,
(SELECT 'кур' k UNION ALL SELECT 'курец' UNION ALL SELECT 'курове' UNION ALL SELECT 'кура' UNION ALL SELECT 'kur' UNION ALL SELECT 'kure' UNION ALL SELECT 'kura') x
WHERE g.group_name = 'kur';

INSERT INTO keywords (keyword, group_id)
SELECT k, g.id FROM keyword_groups g,
(SELECT 'useless' k UNION ALL SELECT 'uselessa' UNION ALL SELECT 'юслес' UNION ALL SELECT 'юслеса' UNION ALL SELECT 'ангел' UNION ALL SELECT 'ачо' UNION ALL SELECT 'a4o') x
WHERE g.group_name = 'usl';

INSERT INTO keywords (keyword, group_id)
SELECT k, g.id FROM keyword_groups g,
(SELECT 'бот' k UNION ALL SELECT 'бота' UNION ALL SELECT 'ботче' UNION ALL SELECT 'bot' UNION ALL SELECT 'bota') x
WHERE g.group_name = 'bot';

INSERT INTO keywords (keyword, group_id)
SELECT k, g.id FROM keyword_groups g,
(SELECT 'haralampi' k UNION ALL SELECT 'харалампи') x
WHERE g.group_name = 'haralampi';

INSERT INTO keywords (keyword, group_id)
SELECT k, g.id FROM keyword_groups g,
(SELECT 'сряда' k UNION ALL SELECT 'срядата' UNION ALL SELECT 'wednesday' UNION ALL SELECT 'wensday' UNION ALL SELECT 'wendesday' UNION ALL SELECT 'srqda') x
WHERE g.group_name = 'wednesday';

INSERT INTO keywords (keyword, group_id)
SELECT 'day1', g.id FROM keyword_groups g WHERE g.group_name = 'd1';

INSERT INTO keywords (keyword, group_id)
SELECT k, g.id FROM keyword_groups g,
(SELECT 'цици' k UNION ALL SELECT 'цицки' UNION ALL SELECT 'boobs' UNION ALL SELECT 'cici') x
WHERE g.group_name = 'booba';
