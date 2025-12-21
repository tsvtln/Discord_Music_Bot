# ===== BEGIN OS Commands =====
# Load SSH user and server from conf/bot.conf via DBHelpers (standalone, no circular deps)
from bin.db_helpers import DBHelpers
_conf = DBHelpers.db_conf()
user = _conf.get('SSHUSR', '')
server = _conf.get('S2', '')

allowed_commands = {
    'date': 'date',
    'uptime': 'uptime',
    'cpu_ms': 'ps -eo pid,comm,%cpu --sort=-%cpu | head -n 6',
    'mem_ms': 'ps -eo pid,comm,%mem --sort=-%mem | head -n 6',
    'disk_ms': 'df -h',
    'jelly': f"ssh {user}@{server} 'systemctl status jellyfin.service |head -5'",
    'tailscale_s1': "systemctl status tailscaled.service |head -5",
    'tailscale_s2': f"ssh {user}@{server} 'systemctl status tailscaled.service |head -5'",
    'zabbix_s1': "systemctl status zabbix-server.service |head -5&&"
                 "systemctl status zabbix-agent.service |head -5",
    'zabbix_s2': f"ssh {user}@{server} 'systemctl status zabbix-agent2.service|head -5'",
    'dns': "systemctl status pihole-FTL.service|head -5",
    'cpu_usg_ms': "top -bn1 | awk '/Cpu/ {printf \"%.2f%%\", $2}'",
    'mem_usg_ms': "free -m | awk '/Mem:/ {printf \"%.2f%%\", $3/$2 * 100.0}'",
    'disk_usg_ms': "df -h | awk '$NF==\"/\"{printf \"%.2f%%\", $5}'",
    'mem_usg_js': f"ssh {user}@{server} 'free -m | awk \"/Mem:/ {{printf \\\"%.2f%%\\\", \\$3/\\$2 * 100.0}}\"'",
    'mem_js': f'ssh {user}@{server} "free -m"',
    'cpu_js': f'ssh {user}@{server} "ps -eo pid,comm,%cpu --sort=-%cpu | head -n 6"',
    'cpu_usg_js': f"ssh {user}@{server} 'top -bn1 | awk \"/Cpu/ {{printf \\\"%.2f%%\\\", \\$2}}\"'",
    'disk_js': f'ssh {user}@{server} "df -h"',
    'disk_usg_js': f"ssh {user}@{server} 'df -h | awk \"\\$NF==\\\"/\\\"{{printf \\\"%.2f%%\\\", \\$5}}\"'",
    'temps_ms': "sensors | grep 'Core' | awk '{print $1, $2, $3}' | head -n 6",
    'temps_js': f"ssh {user}@{server} 'sensors | grep \"Core\" | awk \"{{print \\$1, \\$2, \\$3}}\" | head -n 6'",
}

not_allowed = {
    'rm -rf *': 'https://media.giphy.com/media/3XEgV9kfwLy1i/giphy.gif'
}
# ===== END OS Commands =====
