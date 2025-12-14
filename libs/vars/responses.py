# ===== BEGIN Responses =====


def _load_responses(category: str) -> list[str]:
    # Local import avoids circular dependencies at module import time
    from bin.db_helpers import DBHelpers
    rows = DBHelpers.fetch_all(
        "SELECT response_text FROM responses WHERE category = %s AND enabled = TRUE",
        (category,)
    )
    return [row[0] for row in rows]

bot_keywords = _load_responses('bot')
haralampi_keywords = _load_responses('haralampi')
# ===== END Responses =====
