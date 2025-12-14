# ===== BEGIN Status Messages =====


def _load_presence_states() -> list[str]:
    # Local import avoids circular dependencies at module import time
    from bin.db_helpers import DBHelpers
    rows = DBHelpers.fetch_all(
        "SELECT status_text FROM presence_states WHERE enabled = TRUE",
        ()
    )
    return [row[0] for row in rows]

presence_states = _load_presence_states()
# ===== END Status Messages =====
