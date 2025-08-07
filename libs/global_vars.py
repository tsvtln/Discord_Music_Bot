class VARS:
    """
    This class holds the global variables used in the Discord Music Bot.
    """
    from .vars.command_prefixes import command_prefixes
    from .vars.gifs import beer, cheer, booba, kur, usl, its_wednesday, not_wednesday, d1
    from .vars.presence_states import presence_states
    from .vars.responses import funny
    from .vars.os_commands import user, server, allowed_commands, not_allowed
    from .vars.lucky_list import luck_list
    files_to_clean = []

    # --- Keyword GIF and string auto-response ---
    beer_keywords = ['бири', 'бира', 'bira', 'biri', 'beer']
    kur_keywords = ['кур', 'курец', 'курове', 'кура', 'kur', 'kure', 'kura']
    usl_keywords = ['useless', 'uselessa', 'юслес', 'юслеса', 'ангел', 'ачо', 'a4o']
    bot_keywords = ['бот', 'бота', 'ботче', 'bot', 'bota']
    haralampi_keywords = ['haralampi', 'харалампи']
    wednesday_keywords = ['сряда', 'срядата', 'wednesday', 'wensday', 'wendesday', 'srqda']
    d1_keywords = ['day1']