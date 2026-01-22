class VARS:
    """
    This class holds the global variables used in the Discord Music Bot.
    """
    from .vars.command_prefixes import command_prefixes
    from .vars.gifs import beer, cheer, booba, kur, usl, its_wednesday, not_wednesday, d1
    from .vars.presence_states import presence_states
    from .vars.os_commands import user, server, allowed_commands, not_allowed
    from .vars.lucky_list import lucky_list
    from .vars.funny_responses import list_of_funny_not_allowed
    from .vars.responses import bot_keywords as bot_responses
    from .vars.responses import haralampi_keywords as haralampi_responses

    files_to_clean = []
    response_num = 0
    last_message_delta = 0
    last_message_date = 0
    chat_mode = False  # True = AI bot mode, False = database response mode
    debug_mode = False

    @staticmethod
    def users_for_chat_mode() -> list[str]:
        return [
            'potkor',
            'dev40',
            'trogdor3000',
            'delay4106',
            'grimy',
            'джиБъс! - магесник',
            'whoknows (BG)',
            'whoknowsss',
            'tedglil'
        ]

    # Load timeout from DB config (fallback to 3000 if not set)
    @staticmethod
    def _load_timeout() -> int:
        try:
            # Local import to avoid circular dependencies
            from bin.db_helpers import DBHelpers
            row = DBHelpers.fetch_one(
                "SELECT config_value FROM config WHERE config_key = %s LIMIT 1",
                ("timeout",)
            )
            if row and row[0]:
                try:
                    return int(row[0])
                except ValueError:
                    return 3000
            return 3000
        except Exception:
            return 3000

    timeout = _load_timeout()

    # Helper to load keywords by group_name
    @staticmethod
    def _load_keywords(group_name: str) -> list[str]:
        try:
            from bin.db_helpers import DBHelpers
            rows = DBHelpers.fetch_all(
                "SELECT k.keyword FROM keywords k JOIN keyword_groups g ON k.group_id = g.id "
                "WHERE g.group_name = %s AND k.enabled = TRUE",
                (group_name,)
            )
            return [row[0] for row in rows]
        except Exception:
            return []

    # --- Keyword GIF and string auto-response (DB-backed) ---
    beer_keywords = _load_keywords('beer')
    kur_keywords = _load_keywords('kur')
    usl_keywords = _load_keywords('usl')
    bot_keywords = _load_keywords('bot')
    haralampi_keywords = _load_keywords('haralampi')
    wednesday_keywords = _load_keywords('wednesday')
    d1_keywords = _load_keywords('d1')
    booba_keywords = _load_keywords('booba')

    @staticmethod
    def _load_allowed_commands_list() -> list[str]:
        try:
            from bin.db_helpers import DBHelpers
            rows = DBHelpers.fetch_all(
                "SELECT command, description FROM allowed_commands_list ORDER BY id ASC",
                ()
            )
            formatted = []
            for cmd, desc in rows:
                if desc is None or str(desc).strip() == "":
                    formatted.append(cmd)
                else:
                    formatted.append(f"{cmd} - {desc}")
            return formatted
        except Exception:
            return []

    # --- Allowed OS commands list (DB-backed) ---
    allowed_commands_list = _load_allowed_commands_list()

    @staticmethod
    def _load_list_of_commands() -> list[str]:
        try:
            from bin.db_helpers import DBHelpers
            rows = DBHelpers.fetch_all(
                "SELECT command, description FROM list_of_commands ORDER BY id ASC",
                ()
            )
            return [f"{cmd} {desc}" for (cmd, desc) in rows]
        except Exception:
            return []

    # --- List of commands for the bot (DB-backed) ---
    list_of_commands = _load_list_of_commands()

    @staticmethod
    def _load_custom_user_data():
        try:
            from bin.db_helpers import DBHelpers
            rows = DBHelpers.fetch_all(
                "SELECT user_key, user_value FROM custom_user_data",
                ()
            )
            return {user: data for (user, data) in rows}
        except Exception:
            return {}

    # --- Custom user data (DB-backed) ---
    custom_user_data = _load_custom_user_data()

