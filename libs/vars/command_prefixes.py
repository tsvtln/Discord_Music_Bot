# ===== BEGIN Command Prefixes =====
def _load_command_prefixes() -> list[str]:
    # Local import avoids circular dependencies at module import time
    from bin.db_helpers import DBHelpers
    rows = DBHelpers.fetch_all(
        "SELECT command FROM command_prefixes WHERE enabled = TRUE ORDER BY id ASC",
        ()
    )

    return [row[0] for row in rows]


command_prefixes = _load_command_prefixes()
# ===== END Command Prefixes =====
