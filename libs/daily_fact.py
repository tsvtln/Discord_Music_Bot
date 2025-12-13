import requests
import os
from datetime import datetime
import random

FALLBACK_FACTS = [
    "A group of flamingos is called a flamboyance.",
    "Bananas are berries, but strawberries are not.",
    "Honey never spoils.",
    "Octopuses have three hearts.",
    "There are more stars in the universe than grains of sand on Earth."
]

API_URL = 'https://uselessfacts.jsph.pl/api/v2/facts/random'
FACT_DATA_FILE = os.path.join(os.path.dirname(__file__), '../cache/fact_data.txt')


def fetch_fact_from_api():
    try:
        response = requests.get(API_URL, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get('text')
    except Exception:
        pass
    return None


def get_today_fact():
    today = datetime.now().strftime('%Y-%m-%d')
    existing_facts = set()
    # collect all facts for today
    if os.path.exists(FACT_DATA_FILE):
        with open(FACT_DATA_FILE, 'r') as f:
            for line in f:
                if line.startswith(today):
                    fact = line.strip().split('|', 1)[-1]
                    existing_facts.add(fact)
    # try to get a unique fact
    attempts = 0
    max_attempts = 50  # Safety counter
    fact = None
    while attempts < max_attempts:
        fact = fetch_fact_from_api() or random.choice(FALLBACK_FACTS)
        if fact not in existing_facts:
            with open(FACT_DATA_FILE, 'a') as f:
                f.write(f"{today}|{fact}\n")
            return fact
        attempts += 1
    # if all attempts failed, just return a random fallback fact (not saved)
    return random.choice(FALLBACK_FACTS)