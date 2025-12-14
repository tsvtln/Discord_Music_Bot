-- Responses
CREATE TABLE IF NOT EXISTS responses (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(64) NOT NULL,
    response_text VARCHAR(255) NOT NULL,
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_category (category),
    INDEX idx_enabled (enabled)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO responses (category, response_text) VALUES
('bot', 'Не съм! Истински чувек сам!'),
('bot', 'Да бъдеш б0т или да не бъдеш б0т, това ли е въпроса?'),
('bot', 'Ти па си Ален Делон'),
('bot', 'Не съм б0т, ти си б0т!'),
('bot', '1001010101110001011001'),
('bot', 'Виждал съм б0тове ама няма'),
('bot', 'Тука няма б0тове, само истински хора сме'),
('bot', 'Б0т съм, ама не съм б0т'),
('bot', 'От б0та мляко не става'),
('bot', 'През 7 б0та в 8-мия се ражда човек'),
('bot', 'Щи каа аз кой е б0т, ама не е тука'),
('bot', 'Б0т съм, ама не съм б0т, ама съм б0т');

INSERT INTO responses (category, response_text) VALUES
('haralampi', 'Къде? Кой? Кога?'),
('haralampi', 'Я съм Хараламбиии, аа или пък не. Ба ли го.'),
('haralampi', 'Кой е тоя Харамбиии? Аз съм Харамбиии!'),
('haralampi', 'Ура за мен!'),
('haralampi', 'Хараламби, Хараламби, Хараламби! Да живее Хараламби!'),
('haralampi', 'Аз коги съм Харалампял, ти си бил нещо си, не знам, забравих си мисълта.');

