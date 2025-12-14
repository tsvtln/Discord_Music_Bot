-- Allowed OS commands
CREATE TABLE IF NOT EXISTS allowed_commands_list (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    command VARCHAR(255) NOT NULL UNIQUE,
    description VARCHAR(255) DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO allowed_commands_list (command, description) VALUES
('date', NULL),
('uptime', NULL),
('cpu_ms', 'Top 5 CPU consuming processes media server'),
('cpu_usg_ms', 'CPU usage media server'),
('cpu_js', 'Top 5 CPU consuming processes jelly server'),
('cpu_usg_js', 'CPU usage jelly server'),
('mem_ms', 'Top 5 Memory consuming processes media server'),
('mem_usg_ms', 'Memory usage media server'),
('mem_usg_js', 'Memory usage jelly server'),
('mem_js', 'Top 5 Memory consuming processes jelly server'),
('disk_ms', 'Disk usage media server'),
('disk_usage_ms', 'Disk usage media server'),
('disk_js', 'Disk usage jelly server'),
('disk_usage_js', 'Disk usage jelly server'),
('tailscale_s1', 'Check Tailscale status Media Server'),
('tailscale_s2', 'Check Tailscale status Jelly Server'),
('jelly', 'Check Jellyfin status'),
('zabbix_s1', 'Check Zabbix status on media server'),
('zabbix_s2', 'Check Zabbix status on jelly server'),
('dns', 'Check DNS status');

