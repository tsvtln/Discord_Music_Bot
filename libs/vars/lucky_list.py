# ===== BEGIN kusmetcheta =====
# ===== BEGIN Lucky List (DB-backed) =====

def _load_lucky_list() -> list[str]:
    # Local import avoids circular dependencies at module import time
    from bin.db_helpers import DBHelpers
    rows = DBHelpers.fetch_all(
        "SELECT fortune_text FROM lucky_list ORDER BY id ASC",
        ()
    )
    return [row[0] for row in rows]

lucky_list = _load_lucky_list()
# ===== END Lucky List (DB-backed) =====
# ===== END kusmetcheta =====
