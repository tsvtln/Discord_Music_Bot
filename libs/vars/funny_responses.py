# --- List of funny not allowed responses (DB-backed) ---

def _load_funny_responses() -> list[str]:
    # Local import avoids circular dependencies at module import time
    from bin.db_helpers import DBHelpers
    rows = DBHelpers.fetch_all(
        "SELECT response FROM funny_responses WHERE enabled = TRUE ORDER BY id ASC",
        ()
    )
    return [row[0] for row in rows]


list_of_funny_not_allowed = _load_funny_responses()

