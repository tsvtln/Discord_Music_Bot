# This file contains lists and mappings for GIFs and string responses used by the Discord bot.
# We import this file in the main bot code to keep LoFi_bot.py clean.

from decouple import config

# ===== BEGIN GIFs =====
beer = [
    'https://media.giphy.com/media/wKSnAdyvKHKHS/giphy.gif',
    'https://media.giphy.com/media/lTGLOH7ml3poQ6JoFg/giphy.gif',
    'https://media.giphy.com/media/QTgzmGzanMnhiwsBql/giphy.gif',
    'https://media.giphy.com/media/l0HlTocc7w1xFoz6g/giphy.gif',
    'https://media.giphy.com/media/1esoXMqqOjYGm5Bdqt/giphy.gif',
    'https://media.giphy.com/media/9GJ2w4GMngHCh2W4uk/giphy.gif',
    'https://media.giphy.com/media/zTB68FHqA6VRS/giphy.gif',
    'https://media.giphy.com/media/3oEjHNSN9EhhBi2QJq/giphy.gif',
    'https://media4.giphy.com/media/26tP21xUQnOCIIoFi/giphy.gif',
    'https://media.giphy.com/media/2AM7sBtPHGTL5r5WFV/giphy.gif',
]

cheer = [
    'https://media.giphy.com/media/Zw3oBUuOlDJ3W/giphy.gif',
    'https://media.giphy.com/media/4Tkagznwgrv6A4asQb/giphy.gif',
    'https://media.giphy.com/media/l0ExgfAdB2Z9V35hS/giphy.gif',
    'https://media.giphy.com/media/RBx8fOTbEmC8iy27Ki/giphy.gif',
    'https://media.giphy.com/media/TujSrrPYXqeAdPnvuh/giphy.gif',
    'https://media.giphy.com/media/GvlQffBPPLygHFd43p/giphy.gif',
    'https://media.giphy.com/media/hfKTf4RvJJRHL70Zvo/giphy.gif',
    'https://media.giphy.com/media/l0MYHCPKJ9H2VmRyg/giphy.gif',
    'https://media.giphy.com/media/dXFd3q0msGpMjgNEls/giphy.gif',
    'https://media.giphy.com/media/cEYFeDYAEZ974cOS8CY/giphy.gif',
]

booba = [
    'https://media4.giphy.com/media/28A92fQr8uG6Q/giphy.gif',
    'https://media.giphy.com/media/HjlKKc14d5tBK/giphy.gif',
    'https://media.giphy.com/media/l378p60yRSCeVoyAM/giphy.gif',
    'https://media2.giphy.com/media/QscGFjzLHXVg4/giphy.gif',
    'https://media.giphy.com/media/9R2C1v4Y91pp6/giphy.gif',
    'https://media.giphy.com/media/Q1Q2BRA7CXDGg/giphy.gif',
    'https://media.giphy.com/media/tQrweyYjPGPjq/giphy.gif',
]

kur = [
    'https://media4.giphy.com/media/Qc8GJi3L3Jqko/giphy.gif',
    'https://media.giphy.com/media/zCOY3loJHTnfG/giphy.gif',
    'https://media.giphy.com/media/okEAjcVdCLl4I/giphy.gif',
    'https://media.giphy.com/media/1fkdaiYSkzKGM2a3Wj/giphy.gif',
    'https://media.giphy.com/media/l3vRhvmSOagowtJ96/giphy.gif',
    'https://media.giphy.com/media/ybpps0dQwaXf2/giphy.gif',
]

usl = [
    'https://media.giphy.com/media/dQ5XTlqXTysQdGVdWB/giphy.gif',
    'https://media.giphy.com/media/6JSihSBLPqS1VhO9i2/giphy.gif',
    'https://media.giphy.com/media/iScdi2qu0xfGr8chJq/giphy.gif',
    'https://media.giphy.com/media/R9cQo06nQBpRe/giphy.gif',
    'https://media.giphy.com/media/Gtnf8Fok8An9m/giphy.gif',
]

its_wednesday = [
    'https://64.media.tumblr.com/47d8fcdc9ff224e4621a07acd605848a/tumblr_ou5pz8N1kh1wubnyeo1_r1_250.gif'
]

not_wednesday = [
    'https://preview.redd.it/'
    'wukhr6ylhjo41.png?width=640&crop=smart&auto=webp&s=6d249d495cfd5cdcecd2ab0b08fae0e80b3ff35c',
    'https://i.pinimg.com/736x/79/b7/84/79b784792d35c304af077ee2e450eea1.jpg',
    'https://media.tenor.com/80plcYSqPQsAAAAC/no-its-not-nope.gif',
]

# ===== END GIFs =====

# ===== BEGIN Status Messages =====
presence_states = [
    'цигу-мигу, чака-рака',
    'Биряна ми изпи Бирата',
    'Морския е морски човек',
    'Пиян съм, не ме питайте',
    'Кой е харалампи',
    'Аз не съм бот, ти си бот',
    'Пия малко, повръщам много',
    'Юслеса яде лайна',
    'Лайната не ядат юслеса',
    'Уше със шише, на суши се шосе...',
    'Утре е преди днес',
    'Вчера е преди утрето на днеската',
    'Тука има локва',
    'Как се кара кола?',
    'Блъснах се в дърво, ама не е мое',
    'Кой е този човек?',
    'Кой е този човек, който не е човек?',
    'Кой е този човек, който не е човек, а е бот?',
    'Кой е този човек, който не е човек, а е бот, и не е тук?',
    'Кой е този човек, който не е човек, а е бот, и не е тук, и не пее?',
    'Кой е този човек, който не е човек, а е бот, и не е тук, и не пее, и не пие бира?',
    'Тутманик с бира е най-добрия тутманик',
    'Бира с тутманик е най-добрата бира',
    'Бира с бира е най-добрата бира',
    'Голямото малко е по-голямо от малкото голямо',
    'Крава пие мляко, а козата яде сено',
    'Малък сечко, голямо сечко',
    'Сецам бавно, тичам бързо',
]
# ===== END Status Messages =====

# ===== BEGIN Responses =====
funny = [
    'Не съм! Истински чувек сам!',
    'Къде? Кой? Кога?',
]
# ===== END Responses =====

# ===== BEGIN OS Commands =====
user = config('SSHUSR')
server = config('S2')

allowed_commands = {
    'date': 'date',
    'uptime': 'uptime',
    'cpu_ms': 'ps -eo pid,comm,%cpu --sort=-%cpu | head -n 6',
    'mem_ms': 'ps -eo pid,comm,%mem --sort=-%mem | head -n 6',
    'disk': 'df -h',
    'jelly': f"ssh {user}@{server} 'systemctl status jellyfin.service |head -5'",
    'tailscale_s1': "systemctl status tailscaled.service |head -5",
    'tailscale_s2': f"ssh {user}@{server} 'systemctl status tailscaled.service |head -5'",
    'zabbix_s1': "systemctl status zabbix-server.service |head -5&&"
                 "systemctl status zabbix-agent.service |head -5",
    'zabbix_s2': f"ssh {user}@{server} 'systemctl status zabbix-agent2.service|head -5'",
    'dns': "systemctl status maradns.service|head -5",
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

fruits = ["apple", "banana", "cherry", "date", "elderberry"]

