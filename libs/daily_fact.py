import requests
import random
from typing import Set, List

API_URL = 'https://uselessfacts.jsph.pl/api/v2/facts/random'


def _get_fallback_facts() -> List[str]:
    from bin.db_helpers import DBHelpers
    rows = DBHelpers.fetch_all("SELECT fact_text FROM fallback_facts WHERE enabled = TRUE")
    return [row[0] for row in rows]


def _get_today_existing_facts() -> Set[str]:
    from bin.db_helpers import DBHelpers
    rows = DBHelpers.fetch_all("SELECT fact_text FROM fact_data WHERE DATE(added_at) = CURDATE()")
    return {row[0] for row in rows}


def _store_fact_today(fact_text: str) -> None:
    from bin.db_helpers import DBHelpers
    DBHelpers.execute("INSERT INTO fact_data (fact_text) VALUES (%s)", (fact_text,))


def fetch_fact_from_api():
    try:
        response = requests.get(API_URL, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get('text')
    except Exception:
        pass
    return None


def get_today_fact() -> str:
    existing_facts = _get_today_existing_facts()
    fallbacks = _get_fallback_facts() or [
        "A group of flamingos is called a flamboyance.",
        "Bananas are berries, but strawberries are not.",
        "Honey never spoils.",
        "Octopuses have three hearts.",
        "There are more stars in the universe than grains of sand on Earth."
    ]

    attempts = 0
    max_attempts = 50
    while attempts < max_attempts:
        fact = fetch_fact_from_api() or random.choice(fallbacks)
        if fact and fact not in existing_facts:
            _store_fact_today(fact)
            return fact
        attempts += 1
    return random.choice(fallbacks)
