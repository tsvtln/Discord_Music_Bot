# ===== BEGIN GIFs =====

# DB-backed loader for GIF URLs by category

def _load_gifs(category: str) -> list[str]:
    # Local import avoids circular dependencies at module import time
    from bin.db_helpers import DBHelpers
    rows = DBHelpers.fetch_all(
        "SELECT gif_url FROM gifs WHERE category = %s AND enabled = TRUE ORDER BY id ASC",
        (category,)
    )
    return [row[0] for row in rows]

# Public lists populated from DB
beer = _load_gifs('beer')
cheer = _load_gifs('cheer')
booba = _load_gifs('booba')
kur = _load_gifs('kur')
usl = _load_gifs('usl')
its_wednesday = _load_gifs('its_wednesday')
not_wednesday = _load_gifs('not_wednesday')
d1 = _load_gifs('d1')

# ===== END GIFs =====
