class VARS:
    """
    This class holds the global variables used in the Discord Music Bot.
    """
    from .vars.command_prefixes import command_prefixes
    from .vars.gifs import beer, cheer, booba, kur, usl, its_wednesday, not_wednesday, d1
    from .vars.presence_states import presence_states
    from .vars.os_commands import user, server, allowed_commands, not_allowed
    from .vars.lucky_list import luck_list
    from .vars.funny_responses import list_of_funny_not_allowed
    from .vars.responses import bot_keywords as bot_responses
    from .vars.responses import haralampi_keywords as haralampi_responses

    files_to_clean = []
    response_num = 0
    last_message_delta = 0
    last_message_date = 0
    timeout = 3000

    # --- Keyword GIF and string auto-response ---
    beer_keywords = ['бири', 'бира', 'bira', 'biri', 'beer']
    kur_keywords = ['кур', 'курец', 'курове', 'кура', 'kur', 'kure', 'kura']
    usl_keywords = ['useless', 'uselessa', 'юслес', 'юслеса', 'ангел', 'ачо', 'a4o']
    bot_keywords = ['бот', 'бота', 'ботче', 'bot', 'bota']
    haralampi_keywords = ['haralampi', 'харалампи']
    wednesday_keywords = ['сряда', 'срядата', 'wednesday', 'wensday', 'wendesday', 'srqda']
    d1_keywords = ['day1']
    booba_keywords = ['цици', 'цици', 'цицки', 'boobs', 'cici']

    # --- Allowed OS commands list ---
    allowed_commands_list = [
        'date',
        'uptime',
        'cpu_ms - Top 5 CPU consuming processes media server',
        'cpu_usg_ms - CPU usage media server',
        'cpu_js - Top 5 CPU consuming processes jelly server',
        'cpu_usg_js - CPU usage jelly server',
        'mem_ms - Top 5 Memory consuming processes media server',
        'mem_usg_ms - Memory usage media server',
        'mem_usg_js - Memory usage jelly server',
        'mem_js - Top 5 Memory consuming processes jelly server',
        'disk_ms - Disk usage media server',
        'disk_usage_ms - Disk usage media server',
        'disk_js - Disk usage jelly server',
        'disk_usage_js - Disk usage jelly server',
        'tailscale_s1 - Check Tailscale status Media Server',
        'tailscale_s2 - Check Tailscale status Jelly Server',
        'jelly - Check Jellyfin status',
        'zabbix_s1 - Check Zabbix status on media server',
        'zabbix_s2 - Check Zabbix status on jelly server',
        'dns - Check DNS status',
    ]

    # --- List of commands for the bot ---
    list_of_commands = [
        '$play (url или име на песен) - Пуща песен',
        '$pause - Палза',
        '$stop - Спира песента и трие све',
        '$resume - Пуща паузираната песен',
        '$queue - Показва плейлиста',
        '$weather <град> - Показва времето в града. Пример: $weather Sofia',
        '$weather5 <град> - Показва 5-дневна прогноза за времето в града. Пример: $weather5 Sofia',
        '$kysmetche - Дръпни си късметчето за деня',
        '$kysmetche reroll - Ако вече си дръпнал късметче, можеш да си го реролнеш'
    ]
