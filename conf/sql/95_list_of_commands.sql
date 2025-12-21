-- Bot commands list
CREATE TABLE IF NOT EXISTS list_of_commands (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    command VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO list_of_commands (command, description) VALUES
('$play', '(url или име на песен) - Пуща песен'),
('$pause', 'Палза'),
('$stop', 'Спира песента и трие све'),
('$resume', 'Пуща паузираната песен'),
('$queue', 'Показва плейлиста'),
('$weather', '<град> - Показва времето в града. Пример: $weather Sofia'),
('$weather5', '<град> - Показва 5-дневна прогноза за времето в града. Пример: $weather5 Sofia'),
('$weather15', '<град> - Показва 15-дневна прогноза за времето в града. Пример: $weather15 Sofia'),
('$kysmetche', 'Дръпни си късметчето за деня'),
('$kysmetche reroll', 'Ако вече си дръпнал късметче, можеш да си го реролнеш'),
('$ChatMode', 'Включва или изключва чат бот AI отговори в този канал.');

